from fastapi import FastAPI, HTTPException, Depends, Request, Form
from db_config import get_db
from models import Client, Product, Employee
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from datetime import date
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from schemas import ClientCreate, ProductCreate, EmployeeCreate
from typing import List

templates = Jinja2Templates(directory="templates")

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def nav_page(request: Request):
    return templates.TemplateResponse("nav.html", {"request": request})


@app.get(
    "/clients",
    tags=["Client"],
    summary="Получить клиентов",
    response_class=HTMLResponse,
)
def gets_clients(request: Request, db=Depends(get_db)):
    clients = db.query(Client).all()
    return templates.TemplateResponse(
        "client.html", {"request": request, "clients": clients}
    )


@app.get("/client/{client_id}", tags=["Client"], summary="Получить клиента")
def get_client(id: int, db: Session = Depends(get_db)):
    res = db.scalar(select(Client).where(Client.client_id == id))
    if res is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return res


@app.post("/client", tags=["Client"], summary="Добавить клиента")
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


@app.post("/clients/delete/{client_id}")
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    # client = db.query(Client).filter(Client.client_id == client_id).first()
    client = db.scalar(select(Client).where(Client.client_id == client_id))
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    db.delete(client)
    db.commit()

    return RedirectResponse(url="/clients", status_code=303)


@app.post(
    "/clients/delete_selected",
    response_class=HTMLResponse,
)
def delete_clients(
    selected_items: List[int] = Form(...), db: Session = Depends(get_db)
):
    # clients = db.query(Client).filter(Client.client_id.in_(selected_clients)).delete()
    #
    # if not clients:
    #     raise HTTPException(status_code=404, detail="Клиенты не найдены")
    #
    # db.delete(clients)
    # db.commit()
    #
    # return RedirectResponse(url="/clients", status_code=303)
    try:
        if not selected_items:
            return RedirectResponse(url="/clients", status_code=303)

        # Удаляем всех выбранных клиентов
        db.query(Client).filter(Client.client_id.in_(selected_items)).delete()
        db.commit()

        return RedirectResponse(url="/clients", status_code=303)

    except Exception as e:
        db.rollback()
        return RedirectResponse(url="/clients", status_code=303)


@app.put("/client", tags=["Client"], summary="Обновить клиента")
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


@app.get(
    "/product",
    tags=["Product"],
    summary="Получить продукты",
    response_class=HTMLResponse,
)
def get_products(request: Request, db=Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse(
        "product.html", {"request": request, "products": products}
    )


@app.get("/product/{product_id}", tags=["Product"], summary="Получить продукт")
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@app.post("/product", tags=["Product"], summary="Добавить продукт")
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        product_name=product.product_name,
        description=product.description,
        rate=product.rate,
        term=product.term,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.delete("/product", tags=["Product"], summary="Удалить продукт")
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return product


@app.put("/product", tags=["Product"], summary="Обновить продукт")
def update_product(
    id: int,
    product_name: str,
    description: str,
    rate: str,
    term: str,
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.product_id == id)

    if product_name is not None:
        product_name = product_name

    if description is not None:
        description = description

    if rate is not None:
        rate = rate

    if term is not None:
        term = term

    db.refresh(product)
    db.commit()


@app.get("/employee", tags=["Employee"], summary="Получить сотрудников")
def get_employees(request: Request, db=Depends(get_db)):
    emp = db.query(Employee).all()
    return templates.TemplateResponse(
        "employee.html", {"request": request, "employees": emp}
    )


@app.get("/employee/{employee_id}", tags=["Employee"], summary="Получить сотрудника")
def get_employee(id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.employee_id == id)

    if emp is None:
        raise HTTPException(status_code=404, detail="Employee  not found")

    return emp


@app.post("/employee", tags=["Employee"], summary="Добавить сотрудника")
def add_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_emp = Employee(
        full_name=employee.full_name,
        position=employee.position,
        hire_date=employee.hire_date,
    )
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp


@app.delete("/employee", tags=["Employee"], summary="Удалить сотрудника")
def delete_emp(id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.employee_id == id)

    if emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(emp)
    db.commit()
    return emp


@app.put("/employee", tags=["Employee"], summary="Обновить сотрудника")
def update_emp(
    id: int,
    full_name: str,
    position: str,
    hire_date: date,
    db: Session = Depends(get_db),
):
    emp = db.query(Employee).filter(Employee.employee_id == id)

    if full_name is not None:
        full_name = full_name
    if position is not None:
        position = position
    if hire_date is not None:
        hire_date = hire_date
    db.refresh(emp)
    db.commit()
    return emp
