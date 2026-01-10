from fastapi import HTTPException, Depends, Request, APIRouter
from db import get_db
from models import Employee
from sqlalchemy.orm import Session
from datetime import date
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from schemas import EmployeeCreate

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix='/employee', tags=['Employees'])

@router.get("/get", summary="Получить сотрудников")
def get_employees(request: Request, db=Depends(get_db)):
    emp = db.query(Employee).all()
    return templates.TemplateResponse(
        "employee.html", {"request": request, "employees": emp}
    )


@router.get("/get/{employee_id}", tags=["Employee"], summary="Получить сотрудника")
def get_employee(id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.employee_id == id)

    if emp is None:
        raise HTTPException(status_code=404, detail="Employee  not found")

    return emp


@router.post("/add", summary="Добавить сотрудника")
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


@router.delete("/delete", summary="Удалить сотрудника")
def delete_emp(id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.employee_id == id)

    if emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(emp)
    db.commit()
    return emp


@router.put("/update", summary="Обновить сотрудника")
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
