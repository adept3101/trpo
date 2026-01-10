from fastapi import HTTPException, Depends, Request, Form, Query, APIRouter
from db import get_db
from models import Client
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from schemas import ClientCreate
from typing import List

templates = Jinja2Templates(directory="templates")

router =  APIRouter(prefix='/clients', tags=['Clients'])

@router.get(
    "/",
    summary="Получить клиентов",
    response_class=HTMLResponse,

)
def gets_clients(request: Request, db=Depends(get_db), search: str = Query(None)):
    # clients = db.query(Client).all()

    query = db.query(Client)
    if search:
        query = query.filter(Client.name.ilike(f"%{search}%"))

    clients = query.all()
    return templates.TemplateResponse(
        "client.html", {"request": request, "clients": clients}
    )


@router.get("/{client_id}", summary="Получить клиента")
def get_client(id: int, db: Session = Depends(get_db)):
    # res = db.scalar(select(Client).where(Client.client_id == id))
    res = db.query(Client).filter(Client.client_id == id)
    if res is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return res


@router.post("/add")
def add_client_from_form(
    request: Request,
    name: str = Form(...),
    lastname: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    db: Session = Depends(get_db),
):
    existing_client = db.query(Client).filter(Client.email == email).first()
    if existing_client:
        clients = db.query(Client).all()
        return templates.TemplateResponse(
            "client.html",
            {
                "request": request,
                "clients": clients,
                "error": "Клиент с таким email уже существует",
            },
        )

    new_client = Client(name=name, lastname=lastname, email=email, phone=phone)

    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return RedirectResponse(url="/clients", status_code=303)


@router.post("/_add", summary="Добавить клиента")
def add_client(client: ClientCreate, db: Session = Depends(get_db)):
    cl = db.query(Client).filter(Client.email == client.email).first()
    if cl:
        raise HTTPException(status_code=400, detail="Email is used")

    new_client = Client(
        name=client.name,
        lastname=client.lastname,
        phone=client.phone,
        email=client.email,
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


@router.post("/delete/{client_id}")
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.client_id == client_id)
    # client = db.scalar(select(Client).where(Client.client_id == client_id))
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    db.delete(client)
    db.commit()

    return RedirectResponse(url="/clients", status_code=303)


@router.post(
    "/delete_selected",
    response_class=HTMLResponse,
)
def delete_clients(
    selected_items: List[int] = Form(...), db: Session = Depends(get_db)
):
    try:
        if not selected_items:
            return RedirectResponse(url="/clients", status_code=303)

        db.query(Client).filter(Client.client_id.in_(selected_items)).delete()
        db.commit()

        return RedirectResponse(url="/clients", status_code=303)

    except:
        db.rollback()
        return RedirectResponse(url="/clients", status_code=303)


@router.put("/upd", summary="Обновить клиента")
def update_client(
    id: int,
    name: str,
    lastname: str,
    phone: str,
    email: str,
    registr_data: str,
    db: Session = Depends(get_db),
):
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
