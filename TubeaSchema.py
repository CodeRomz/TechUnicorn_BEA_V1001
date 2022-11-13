from pydantic import BaseModel, Field, EmailStr
from datetime import datetime



class UserSchema(BaseModel):
    user_id: int = Field(...)
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    access: str = Field(...)

class AppointmentSchema(BaseModel):
    doctor_id: int = Field(...)
    patient_id: int = Field(...)
    # date: datetime = Field(...)
    # start_time: datetime = Field(...)
    # end_time: datetime = Field(...)
    # running_time: datetime = Field(...)
    date: str = Field(...)
    start_time: str = Field(...)
    end_time: str = Field(...)
    status: str = Field(...)

