from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
# import re


class ClientCreate(BaseModel):
    name: str = Field(max_length=32, pattern=r"^[а-яА-Яa-zA-Z]+$")
    lastname: str = Field(max_length=32, pattern=r"^[а-яА-Яa-zA-Z]+$")
    phone: str = Field(pattern=r"^(?:\+7|8)\d{10}$")
    email: EmailStr
    # registr_date: datetime


class ProductCreate(BaseModel):
    product_name: str = Field(min_length=3, max_length=64)
    description: str = Field(max_length=255)
    rate: str = Field(max_length=64)
    term: str = Field(max_length=64)


class EmployeeCreate(BaseModel):
    full_name: str = Field(pattern=r"^[а-яА-Яa-zA-Z\s]+$")
    position: str = Field(max_length=32)
    hire_date: datetime
