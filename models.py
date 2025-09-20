from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, MappedColumn
from db_config import Base


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


__table_args__ = {"extend_existing": True}
