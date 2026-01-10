from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import clients, employee, products
from  auth import auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clients.router)
app.include_router(products.router)
app.include_router(employee.router)
app.include_router(auth.router)
