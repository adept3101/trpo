from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, MappedColumn
from db_config import Base
from datetime import date


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


class Client_product(Base):
    __tablename__ = "client_product"

    client_id: Mapped[int] = MappedColumn(
        ForeignKey("client.client_id"), primary_key=True
    )
    product_id: Mapped[int] = MappedColumn(
        ForeignKey("product.product_id"), primary_key=True
    )
    start_date: Mapped[date] = MappedColumn()
    end_date: Mapped[date] = MappedColumn()
    status: Mapped[str] = MappedColumn()


class Passport(Base):
    __tablename__ = "passport"

    passport_id: Mapped[int] = MappedColumn(primary_key=True)
    client_id: Mapped[int] = MappedColumn(ForeignKey("client.client_id"))
    series: Mapped[str] = MappedColumn()
    number: Mapped[str] = MappedColumn()
    iss_date: Mapped[date] = MappedColumn()


class Application(Base):
    __tablename__ = "passport"

    application_id: Mapped[int] = MappedColumn(primary_key=True)
    client_id: Mapped[int] = MappedColumn(ForeignKey("client.client_id"))
    product_id: Mapped[int] = MappedColumn(
        ForeignKey("product.product_id"), primary_key=True
    )
    employee_id: Mapped[int] = MappedColumn(
        ForeignKey("employee.employee_id"), primary_key=True
    )
    status: Mapped[str] = MappedColumn()
    application_data: Mapped[str] = MappedColumn()


class Account(Base):
    __tablename__ = "account"

    account_id: Mapped[int] = MappedColumn(primary_key=True)
    client_id: Mapped[int] = MappedColumn(
        ForeignKey("client.client_id"), primary_key=True
    )
    numver_acc: Mapped[int] = MappedColumn()
    balance: Mapped[int] = MappedColumn()
    currency: Mapped[int] = MappedColumn()
    open_data: Mapped[str] = MappedColumn()


class Transaction(Base):
    __tablename__ = "transaction"

    transaction_id: Mapped[int] = MappedColumn(primary_key=True)
    account_id: Mapped[int] = MappedColumn(ForeignKey("account.account_id"))
    amount: Mapped[int] = MappedColumn()
    transaction_data: Mapped[str] = MappedColumn()
    type: Mapped[str] = MappedColumn()


class Account_product(Base):
    __tablename__ = "account_product"

    account_id: Mapped[int] = MappedColumn(
        ForeignKey("account.account_id"), primary_key=True
    )
    product_id: Mapped[int] = MappedColumn(ForeignKey("product.product_id"))
    data_connect: Mapped[str] = MappedColumn()
    status: Mapped[str] = MappedColumn()


__table_args__ = {"extend_existing": True}
