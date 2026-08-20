from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

    @field_validator("password")
    @classmethod
    def password_has_letter_and_number(cls, value: str) -> str:
        if not any(c.isalpha() for c in value) or not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one letter and one number")
        return value

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class RegisterOut(BaseModel):
    message: str
    email: EmailStr

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class ServiceIn(BaseModel):
    name: str = Field(min_length=2)
    category: str = Field(min_length=2)
    description: str = Field(min_length=2)
    duration_minutes: int = Field(ge=15, le=480)
    price: float = Field(ge=0)

class ServiceOut(ServiceIn):
    id: int
    active: bool
    model_config = ConfigDict(from_attributes=True)

class AvailabilityIn(BaseModel):
    start_time: datetime
    end_time: datetime

class BookingIn(BaseModel):
    provider_id: int
    service_id: int
    appointment_time: datetime

class BookingUpdate(BaseModel):
    appointment_time: datetime

class BookingOut(BaseModel):
    id: int
    customer_id: int
    provider_id: int
    service_id: int
    appointment_time: datetime
    status: str
    model_config = ConfigDict(from_attributes=True)


