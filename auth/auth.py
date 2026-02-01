from fastapi import Response, HTTPException, Depends, APIRouter, Request, Form
from schemas import UserCreate
from auth.cookie import security, config
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from db import get_db
from models import User
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from argon2 import PasswordHasher

router = APIRouter(prefix="/auth", tags=["Auth"])
templates = Jinja2Templates(directory="templates")

ph = PasswordHasher()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hashed_pass(password: str) -> str:
    hash_pass = ph.hash(password)
    return hash_pass


def verify_pass(password: str, hash_password: str) -> bool:
    return ph.verify(hash_password, password)


@router.get("/items")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request":request})

@router.post("/login")
def login(response: Response,
    creds: UserCreate = Form(...),
    # login: str = Form(...),
    # password: str = Form(...),
    db: Session = Depends(get_db)
          ):
    user = db.query(User).filter(User.login == creds.login).first()
    if not user or not verify_pass(creds.password, user.hash_pass):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    token = security.create_access_token(uid=str(user.id))
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    # return {"access token": token}
    return RedirectResponse("/nav", status_code=303)

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register(reg: UserCreate = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.login == reg.login).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким логином существует"
        )

    hash_ = ph.hash(reg.password)
    new_usr = User(login=reg.login, hash_pass=hash_)
    db.add(new_usr)
    db.commit()
    db.refresh(new_usr)
    #return new_usr
    # return RedirectResponse("/auth/login")
    return RedirectResponse("/auth/login", status_code=303)

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return RedirectResponse("/auth/login", status_code=303)
