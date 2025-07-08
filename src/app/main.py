from fastapi import FastAPI
from app.api.tickets import router as tickets_router

app = FastAPI()
app.include_router(tickets_router, prefix="/tickets")