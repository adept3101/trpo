from fastapi import FastAPI, HTTPException, Depends
from db_config import SessionLocal, get_db
from models import Client, Product, Employee
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from datetime import date

app = FastAPI()


@app.get("/clients", tags=["Client"], summary="Получить клиентов")
def gets_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()


@app.get("/client/{client_id}", tags=["Client"], summary="Получить клиента")
def get_client(id: int, db: Session = Depends(get_db)):
    res = db.scalar(select(Client).where(Client.client_id == id))
    if res is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return res


@app.post("/client", tags=["Client"], summary="Добавить клиента")
def add_client(
    client_id: int,
    name: str,
    lastname: str,
    phone: str,
    email: str,
    registr_data: str,
    db: Session = Depends(get_db),
):
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


@app.delete("/client", tags=["Client"], summary="Удалить клиента")
def delete_client(id: int, db: Session = Depends(get_db)):
    client = db.scalar(select(Client).where(Client.client_id == id))
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()


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


@app.get("/product", tags=["Product"], summary="Получить продукты")
def get_products(db: Session = Depends(get_db)):
    product = db.query(Product).all()
    return product


@app.get("/product/{product_id}", tags=["Product"], summary="Получить продукт")
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@app.post("/product", tags=["Product"], summary="Добавить продукт")
def add_product(
    product_id: int,
    product_name: str,
    description: str,
    rate: str,
    term: str,
    db: Session = Depends(get_db),
):
    new_product = Product(
        product_id=product_id,
        product_name=product_name,
        description=description,
        rate=rate,
        term=term,
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
def get_employees(db: Session = Depends(get_db)):
    emp = db.query(Employee).all()
    return emp


@app.get("/employee/{employee_id}", tags=["Employee"], summary="Получить сотрудника")
def get_employee(id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.employee_id == id)

    if emp is None:
        raise HTTPException(status_code=404, detail="Employee  not found")

    return emp


@app.post("/employee", tags=["Employee"], summary="Добавить сотрудника")
def add_employee(
    employee_id: int,
    full_name: str,
    position: str,
    hire_date: date,
    db: Session = Depends(get_db),
):
    new_emp = Employee(
        employee_id=employee_id,
        full_name=full_name,
        position=position,
        hire_date=hire_date,
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
