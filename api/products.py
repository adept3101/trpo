from fastapi import HTTPException, Depends, Request, APIRouter
from db import get_db
from models import Product
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from schemas import ProductCreate

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix='/product', tags=['Products'])

@router.get(
    "/get",
    summary="Получить продукты",
    response_class=HTMLResponse,
)
def get_products(request: Request, db=Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse(
        "product.html", {"request": request, "products": products}
    )


@router.get("/get/{product_id}", summary="Получить продукт")
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.post("/add", summary="Добавить продукт")
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


@router.delete("/delete", summary="Удалить продукт")
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return product


@router.put("/update", summary="Обновить продукт")
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

