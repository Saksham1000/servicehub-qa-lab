import strawberry
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from .auth import current_user
from .database import get_db
from .models import Booking, Provider, Service

@strawberry.type
class ServiceType:
    id:int; name:str; category:str; description:str

@strawberry.type
class ProviderType:
    id:int; name:str; bio:str

@strawberry.type
class BookingType:
    id:int; customer_id:int; provider_id:int; service_id:int; status:str

@strawberry.type
class Query:
    @strawberry.field
    def services(self,info,search:str|None=None)->list[ServiceType]:
        q=info.context["db"].query(Service).filter(Service.active.is_(True))
        if search:q=q.filter(Service.name.ilike(f"%{search}%"))
        return [ServiceType(id=x.id,name=x.name,category=x.category,description=x.description) for x in q.all()]
    @strawberry.field
    def providers(self,info)->list[ProviderType]: return [ProviderType(id=x.id,name=x.user.name,bio=x.bio) for x in info.context["db"].query(Provider).all()]
    @strawberry.field
    def provider(self,info,id:int)->ProviderType|None:
        x=info.context["db"].get(Provider,id); return ProviderType(id=x.id,name=x.user.name,bio=x.bio) if x else None
    @strawberry.field
    def appointments(self,info)->list[BookingType]:
        user=info.context.get("user")
        if not user: raise PermissionError("Authentication required")
        q=info.context["db"].query(Booking)
        if user.role=="customer":q=q.filter(Booking.customer_id==user.id)
        elif user.role=="provider":q=q.filter(Booking.provider_id==user.provider.id)
        return [BookingType(id=x.id,customer_id=x.customer_id,provider_id=x.provider_id,service_id=x.service_id,status=x.status) for x in q.all()]

async def context(request:Request,db:Session=Depends(get_db)):
    user=None
    header=request.headers.get("authorization","")
    if header.startswith("Bearer "):
        try:user=current_user(header[7:],db)
        except Exception:pass
    return {"request":request,"db":db,"user":user}

schema=strawberry.Schema(query=Query)
