from fastapi import Response, HTTPException, Depends, APIRouter
from schemas import UserCreate
from cookie import security, config
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from db import get_db
from models import User
from sqlalchemy.orm import Session

from argon2 import PasswordHasher

router = APIRouter(prefix="/auth", tags=["Auth"])


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


@router.post("/login")
def login(creds: UserCreate, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == creds.login).first()
    # if creds.login == db.query(Users).filter(Users.login == login) and creds.password == "test":
    if not user or not verify_pass(creds.password, user.password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    token = security.create_access_token(uid=str(user.id))
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    return {"access token": token}


# @router.get(
#     "/protected",
#     dependencies=[Depends(security.access_token_required)],
# )
# async def protected():
#     return {"data": "TOP SECRET"}


@router.post("/register")
def register(reg: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.login == reg.login).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким логином существует"
        )

    hash_pass = ph.hash(reg.password)
    new_usr = User(login=reg.login, password=hash_pass)
    db.add(new_usr)
    db.commit()
    db.refresh(new_usr)
    return new_usr
