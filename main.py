from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import clients
from api import employee
from api import products

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
