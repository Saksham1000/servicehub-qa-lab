from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter
from . import graphql_schema
from .auth import create_token, current_user, hash_password, require_role, verify_password
from .config import QA_BUG_MODE
from .database import Base, SessionLocal, engine, get_db
from .models import Availability, Booking, Provider, Service, User
from .schemas import AvailabilityIn, BookingIn, BookingOut, BookingUpdate, LoginIn, RegisterIn, RegisterOut, ServiceIn, ServiceOut, TokenOut

def seed():
    db = SessionLocal()
    try:
        if db.query(User).count(): return
        admin=User(name="Demo Admin",email="admin@servicehub.example",password_hash=hash_password("Admin123!"),role="admin")
        pu=User(name="Alex Provider",email="provider@servicehub.example",password_hash=hash_password("Provider123!"),role="provider")
        db.add_all([admin,pu]); db.flush()
        provider=Provider(user_id=pu.id,bio="Experienced wellness professional")
        services=[Service(name="Consultation",category="Wellness",description="Personal consultation",duration_minutes=60,price=50),Service(name="Massage",category="Wellness",description="Relaxation massage",duration_minutes=60,price=75),Service(name="Device Repair",category="Technology",description="Device diagnostic and repair",duration_minutes=60,price=90)]
        db.add_all([provider,*services]); db.flush()
        tomorrow=(datetime.now().replace(minute=0,second=0,microsecond=0)+timedelta(days=1))
        db.add_all([Availability(provider_id=provider.id,start_time=tomorrow+timedelta(hours=h),end_time=tomorrow+timedelta(hours=h+1)) for h in range(1,5)])
        db.commit()
    finally: db.close()

@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(engine); seed(); yield

app=FastAPI(title="ServiceHub API",version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

@app.get("/health")
def health(): return {"status":"healthy","bug_mode":QA_BUG_MODE}

@app.post("/api/auth/register",response_model=RegisterOut,status_code=201)
def register(data:RegisterIn,db:Session=Depends(get_db)):
    if db.query(User).filter(func.lower(User.email)==data.email.lower()).first(): raise HTTPException(409,"Email already registered")
    user=User(name=data.name,email=data.email.lower(),password_hash=hash_password(data.password),role="customer")
    db.add(user); db.commit(); db.refresh(user)
    return RegisterOut(message="Account created. Please sign in.",email=user.email)

@app.post("/api/auth/login",response_model=TokenOut)
def login(data:LoginIn,db:Session=Depends(get_db)):
    user=db.query(User).filter(func.lower(User.email)==data.email.lower()).first()
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,"Incorrect email or password")
    return TokenOut(access_token=create_token(user),role=user.role)

@app.get("/api/services",response_model=list[ServiceOut])
def services(search:str|None=None,category:str|None=None,db:Session=Depends(get_db)):
    q=db.query(Service).filter(Service.active.is_(True))
    if search and not QA_BUG_MODE: q=q.filter(func.lower(Service.name).contains(search.lower()))
    if category: q=q.filter(func.lower(Service.category)==category.lower())
    items=q.order_by(Service.name).all()
    return [item for item in items if search in item.name] if QA_BUG_MODE and search else items

@app.get("/api/providers")
def providers(db:Session=Depends(get_db)):
    return [{"id":p.id,"name":p.user.name,"bio":p.bio} for p in db.query(Provider).all()]

@app.get("/api/providers/{provider_id}/availability")
def availability(provider_id:int,db:Session=Depends(get_db)):
    if not db.get(Provider,provider_id): raise HTTPException(404,"Provider not found")
    booked={b.appointment_time for b in db.query(Booking).filter(Booking.provider_id==provider_id,(Booking.status.in_(["confirmed","completed"]) if not QA_BUG_MODE else Booking.status.in_(["confirmed","completed","cancelled"]))).all()}
    return [{"id":a.id,"start_time":a.start_time,"end_time":a.end_time} for a in db.query(Availability).filter(Availability.provider_id==provider_id,Availability.start_time>datetime.now()).all() if a.start_time not in booked]

def validate_slot(db,provider_id,appointment_time,exclude=None):
    if appointment_time<=datetime.now(): raise HTTPException(422,"Appointment must be in the future")
    if not db.query(Availability).filter_by(provider_id=provider_id,start_time=appointment_time).first(): raise HTTPException(409,"Time slot is unavailable")
    if not QA_BUG_MODE:
        q=db.query(Booking).filter(Booking.provider_id==provider_id,Booking.appointment_time==appointment_time,Booking.status.in_(["confirmed","completed"]))
        if exclude: q=q.filter(Booking.id!=exclude)
        if q.first(): raise HTTPException(409,"Provider is already booked")

@app.post("/api/bookings",response_model=BookingOut,status_code=201)
def book(data:BookingIn,user:User=Depends(require_role("customer")),db:Session=Depends(get_db)):
    if not db.get(Service,data.service_id) or not db.get(Provider,data.provider_id): raise HTTPException(404,"Service or provider not found")
    validate_slot(db,data.provider_id,data.appointment_time)
    booking=Booking(customer_id=user.id,**data.model_dump()); db.add(booking)
    try: db.commit(); db.refresh(booking)
    except IntegrityError: db.rollback(); raise HTTPException(409,"Time slot is unavailable")
    return booking

@app.get("/api/bookings/me",response_model=list[BookingOut])
def my_bookings(user:User=Depends(current_user),db:Session=Depends(get_db)):
    if user.role=="provider": return db.query(Booking).filter(Booking.provider_id==user.provider.id).all()
    return db.query(Booking).filter(Booking.customer_id==user.id).all()

def owned_booking(booking_id,user,db):
    booking=db.get(Booking,booking_id)
    if not booking: raise HTTPException(404,"Booking not found")
    allowed=booking.customer_id==user.id or (user.role=="provider" and user.provider and booking.provider_id==user.provider.id) or user.role=="admin"
    if QA_BUG_MODE and user.role=="customer": allowed=True
    if not allowed: raise HTTPException(403,"Booking belongs to another user")
    return booking

@app.patch("/api/bookings/{booking_id}",response_model=BookingOut)
def reschedule(booking_id:int,data:BookingUpdate,user:User=Depends(current_user),db:Session=Depends(get_db)):
    booking=owned_booking(booking_id,user,db); validate_slot(db,booking.provider_id,data.appointment_time,booking.id)
    booking.appointment_time=data.appointment_time; db.commit(); db.refresh(booking); return booking

@app.delete("/api/bookings/{booking_id}",status_code=204)
def cancel(booking_id:int,user:User=Depends(current_user),db:Session=Depends(get_db)):
    booking=owned_booking(booking_id,user,db); booking.status="cancelled"; db.commit(); return Response(status_code=204)

@app.post("/api/provider/availability",status_code=201)
def create_availability(data:AvailabilityIn,user:User=Depends(require_role("provider")),db:Session=Depends(get_db)):
    if data.start_time<=datetime.now() or data.end_time<=data.start_time: raise HTTPException(422,"Invalid availability range")
    slot=Availability(provider_id=user.provider.id,**data.model_dump()); db.add(slot)
    try: db.commit(); db.refresh(slot)
    except IntegrityError: db.rollback(); raise HTTPException(409,"Availability already exists")
    return {"id":slot.id,"start_time":slot.start_time,"end_time":slot.end_time}

@app.patch("/api/provider/bookings/{booking_id}/complete",response_model=BookingOut)
def complete(booking_id:int,user:User=Depends(require_role("provider")),db:Session=Depends(get_db)):
    booking=owned_booking(booking_id,user,db); booking.status="completed"; db.commit(); db.refresh(booking); return booking

@app.get("/api/admin/users")
def admin_users(user:User=Depends(require_role("admin")),db:Session=Depends(get_db)):
    return [{"id":u.id,"name":u.name,"email":u.email,"role":u.role} for u in db.query(User).all()]

@app.get("/api/admin/bookings",response_model=list[BookingOut])
def admin_bookings(user:User=Depends(require_role("admin")),db:Session=Depends(get_db)): return db.query(Booking).all()

@app.post("/api/admin/services",response_model=ServiceOut,status_code=201)
def create_service(data:ServiceIn,user:User=Depends(require_role("admin")),db:Session=Depends(get_db)):
    item=Service(**data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item

@app.patch("/api/admin/services/{service_id}",response_model=ServiceOut)
def update_service(service_id:int,data:ServiceIn,user:User=Depends(require_role("admin")),db:Session=Depends(get_db)):
    item=db.get(Service,service_id)
    if not item: raise HTTPException(404,"Service not found")
    for k,v in data.model_dump().items(): setattr(item,k,v)
    db.commit(); db.refresh(item); return item

@app.delete("/api/admin/services/{service_id}",response_model=ServiceOut)
def deactivate_service(service_id:int,user:User=Depends(require_role("admin")),db:Session=Depends(get_db)):
    item=db.get(Service,service_id)
    if not item: raise HTTPException(404,"Service not found")
    item.active=False; db.commit(); db.refresh(item); return item

app.include_router(GraphQLRouter(graphql_schema.schema,context_getter=graphql_schema.context),prefix="/graphql")





