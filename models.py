from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import Mapped, MappedColumn
from db_config import Base
from datetime import date


class ClientResponse(BaseModel):
    client_id: int
    name: str
    lastname: str
    phone: str
    email: str
    registr_data: str


class Client(Base):
    __tablename__ = "client"

    client_id = Column(Integer, primary_key=True)
    name: Mapped[str] = MappedColumn()
    lastname: Mapped[str] = MappedColumn()
    phone: Mapped[str] = MappedColumn()
    email: Mapped[str] = MappedColumn()
    registr_data: Mapped[str] = MappedColumn()


class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True)
    product_name: Mapped[str] = MappedColumn()
    description: Mapped[str] = MappedColumn()
    rate: Mapped[str] = MappedColumn()
    term: Mapped[str] = MappedColumn()


class Employee(Base):
    __tablename__ = "employee"

    employee_id = Column(Integer, primary_key=True)
    full_name: Mapped[str] = MappedColumn()
    position: Mapped[str] = MappedColumn()
    hire_date: Mapped[date] = MappedColumn(Date)


__table_args__ = {"extend_existing": True}
