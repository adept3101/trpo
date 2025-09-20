from fastapi import FastAPI, HTTPException
from db_config import SessionLocal, get_db
from models import Client
from sqlalchemy.future import select
from typing import Optional

app = FastAPI()


@app.get("/clients")
def gets_clients():
    db = SessionLocal()
    try:
        clients = db.query(Client).all()
        return clients
    finally:
        db.close()


@app.get("/client/{client_id}")
def get_client(id: int):
    db = SessionLocal()
    try:
        res = db.scalar(select(Client).where(Client.client_id == id))

        if res is None:
            raise HTTPException(status_code=404, detail="Client not found")
        return res

    finally:
        db.close()


@app.post("/client", summary="Добавить клиента")
def add_client(
    client_id: int, name: str, lastname: str, phone: str, email: str, registr_data: str
):
    db = SessionLocal()
    try:
        new_client = Client(
            client_id=client_id,
            name=name,
            lastname=lastname,
            phone=phone,
            email=email,
            registr_data=registr_data,
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return new_client
    finally:
        db.close()


@app.delete("/client", summary="Удалить клиента")
def delete_client(id: int):
    db = SessionLocal()
    try:
        client = db.scalar(select(Client).where(Client.client_id == id))
        # search = db.execute(select(Client).where(Client.client_id == id))
        # client = search.scalars().first()
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")
        db.delete(client)
        db.commit()
    finally:
        db.close()


@app.put("/client", summary="Обновить клиента")
def update_client(
    id: int,
    name: str,
    lastname: str,
    phone: str,
    email: str,
    registr_data: str,
):
    db = SessionLocal()
    try:
        # client = db.scalar(select(Client).where(Client.client_id == id))
        # res = db.execute(select(Client).where(Client.client_id == id))
        # client = res.scalar().first()
        client = db.query(Client).filter(Client.client_id == id).first()
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")

        if name is not None:
            client.name = name
        if lastname:
            client.lastname = lastname
        if phone:
            client.phone = phone
        if email:
            client.email = email
        if registr_data:
            client.registr_data = registr_data

        db.commit()
        db.refresh(client)
    finally:
        db.close()
