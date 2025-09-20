from fastapi import FastAPI, HTTPException
from db_config import SessionLocal, get_db
from models import Client
from sqlalchemy.future import select

app = FastAPI()


@app.get("/")
def root():
    return "Hello"


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
        # # client = db.query(Client).where(Client.client_id == id)
        # client = db.execute(select(Client).where(Client.client_id == id))
        # res = client.scalars().first()
        # return client
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
