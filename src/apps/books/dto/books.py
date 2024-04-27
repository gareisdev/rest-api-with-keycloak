from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class LoanStatus(str, Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"
    CANCELED = "canceled"

class BookLoanDTO(BaseModel):
    id: int
    borrower_name: str
    loan_date: str
    due_date: datetime
    return_date: datetime | None = None
    status: str
    notes: str | None = None

class BookDTO(BaseModel):
    id: int
    title: str
    author: str
    publication_year: int
    isbn: str
    genre: str
    quantity: int