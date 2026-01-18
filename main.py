from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from api import clients, employee, products
from auth import auth

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return RedirectResponse("/auth/login")

@app.get("/nav", response_class=HTMLResponse)
def nav(request: Request):
    return templates.TemplateResponse("nav.html", {"request": request})


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
