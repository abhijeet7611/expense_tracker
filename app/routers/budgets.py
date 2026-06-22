from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.dependencies import get_db, get_current_user
from app import models, schemas

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)


# Create Budget
@router.post(
    "/",
    response_model=schemas.BudgetResponse
)
def create_budget(
    budget: schemas.BudgetCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    new_budget = models.Budget(
        month=budget.month,
        year=budget.year,
        amount=budget.amount,
        user_id=current_user
    )

    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)

    return new_budget


# Get All Budgets
@router.get(
    "/",
    response_model=list[schemas.BudgetResponse]
)
def get_budgets(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    budgets = db.query(models.Budget).filter(models.Budget.user_id == current_user).all()
    return budgets


# Remaining Budget Calculator
@router.get("/remaining")
def remaining_budget(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    latest_budget = (
        db.query(models.Budget)
        .filter(models.Budget.user_id == current_user)
        .order_by(models.Budget.id.desc())
        .first()
    )

    if not latest_budget:
        return {
            "message": "No budget found"
        }

    total_expenses = (
        db.query(
            func.sum(models.Expense.amount)
        )
        .filter(models.Expense.user_id == current_user)
        .scalar()
    )

    total_expenses = total_expenses or 0

    remaining = (
        latest_budget.amount -
        total_expenses
    )

    return {
        "budget": latest_budget.amount,
        "spent": total_expenses,
        "remaining": remaining
    }

# Dashboard Summary
@router.get("/dashboard")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    latest_budget = (
        db.query(models.Budget)
        .filter(models.Budget.user_id == current_user)
        .order_by(models.Budget.id.desc())
        .first()
    )

    total_budget = (
        latest_budget.amount
        if latest_budget
        else 0
    )

    total_spent = (
        db.query(
            func.sum(models.Expense.amount)
        )
        .filter(models.Expense.user_id == current_user)
        .scalar()
    )

    total_spent = total_spent or 0

    total_expenses = (
        db.query(models.Expense)
        .filter(models.Expense.user_id == current_user)
        .count()
    )

    remaining_budget = (
        total_budget -
        total_spent
    )

    return {
        "total_budget": total_budget,
        "total_spent": total_spent,
        "remaining_budget": remaining_budget,
        "total_expenses": total_expenses
    }

# Advanced Dashboard Analytics
@router.get("/analytics")
def analytics_dashboard(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    latest_budget = (
        db.query(models.Budget)
        .filter(models.Budget.user_id == current_user)
        .order_by(models.Budget.id.desc())
        .first()
    )

    total_budget = (
        latest_budget.amount
        if latest_budget
        else 0
    )

    total_spent = (
        db.query(
            func.sum(models.Expense.amount)
        )
        .filter(models.Expense.user_id == current_user)
        .scalar()
    )

    total_spent = total_spent or 0

    expense_count = (
        db.query(models.Expense)
        .filter(models.Expense.user_id == current_user)
        .count()
    )

    top_category = (
        db.query(
            models.Expense.category,
            func.sum(models.Expense.amount).label("total")
        )
        .filter(models.Expense.user_id == current_user)
        .group_by(models.Expense.category)
        .order_by(func.sum(models.Expense.amount).desc())
        .first()
    )

    remaining_budget = (
        total_budget -
        total_spent
    )

    return {
        "total_budget": total_budget,
        "total_spent": total_spent,
        "remaining_budget": remaining_budget,
        "expense_count": expense_count,
        "top_category": (
            top_category[0]
            if top_category
            else None
        )
    }