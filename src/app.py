from fastapi import FastAPI, APIRouter
from apps.books.router import router as book_router

app = FastAPI()
app.include_router(book_router)