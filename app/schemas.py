from pydantic import BaseModel, EmailStr
from datetime import date


# ---------------- USER SCHEMAS ---------------- #

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# ---------------- EXPENSE SCHEMAS ---------------- #

class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str
    description: str | None = None
    expense_date: date


class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    description: str | None
    expense_date: date

    class Config:
        from_attributes = True


# ---------------- BUDGET SCHEMAS ---------------- #

class BudgetCreate(BaseModel):
    month: str
    year: int
    amount: float


class BudgetResponse(BaseModel):
    id: int
    month: str
    year: int
    amount: float

    class Config:
        from_attributes = True