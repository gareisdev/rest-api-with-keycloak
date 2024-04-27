from fastapi import APIRouter, Depends
from apps.books.mock.data import books_data, books_loans_data
from apps.books.dto.books import BookDTO, BookLoanDTO
from modules.auth.auth import get_current_user
from typing import List
from fastapi.security import OpenIdConnect

router = APIRouter(prefix="/books")

@router.get("", response_model=List[BookDTO])
async def get_books():
    return books_data

@router.get("/loans", response_model=List[BookLoanDTO])
async def get_books_loans(oidc: OpenIdConnect = Depends(get_current_user)):
    return books_loans_data
