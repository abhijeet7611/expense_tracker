from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.dependencies import (
    get_db,
    get_current_user
)
from app import models, schemas

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


# Create Expense
@router.post(
    "/",
    response_model=schemas.ExpenseResponse
)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(
        get_current_user
    )
):
    new_expense = models.Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        expense_date=expense.expense_date,
        user_id=current_user
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


# Get All Expenses
@router.get(
    "/",
    response_model=list[schemas.ExpenseResponse]
)
def get_expenses(
    db: Session = Depends(get_db),
    current_user: int = Depends(
        get_current_user
    )
):
    return (
    db.query(models.Expense)
    .filter(
        models.Expense.user_id
        == current_user
    )
    .all()
)


# Get Expense By ID
@router.get(
    "/{expense_id}",
    response_model=schemas.ExpenseResponse
)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    expense = (
        db.query(models.Expense)
        .filter(
            models.Expense.id == expense_id,
            models.Expense.user_id == current_user
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense


# Update Expense
@router.put(
    "/{expense_id}",
    response_model=schemas.ExpenseResponse
)
def update_expense(
    expense_id: int,
    updated_expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    expense = (
        db.query(models.Expense)
        .filter(
            models.Expense.id == expense_id,
            models.Expense.user_id == current_user
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    expense.title = updated_expense.title
    expense.amount = updated_expense.amount
    expense.category = updated_expense.category
    expense.description = updated_expense.description
    expense.expense_date = updated_expense.expense_date

    db.commit()
    db.refresh(expense)

    return expense


# Delete Expense
@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    expense = (
        db.query(models.Expense)
        .filter(
            models.Expense.id == expense_id,
            models.Expense.user_id == current_user
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()

    return {
        "message": "Expense deleted successfully"
    }


# Category Wise Report
@router.get("/report/category")
def category_report(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    report = (
        db.query(
            models.Expense.category,
            func.sum(models.Expense.amount).label("total")
        )
        .filter(models.Expense.user_id == current_user)
        .group_by(models.Expense.category)
        .all()
    )

    result = []

    for category, total in report:
        result.append({
            "category": category,
            "total_spent": total
        })

    return result


# Monthly Expense Report
@router.get("/report/monthly")
def monthly_report(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    report = (
        db.query(
            func.extract(
                'month',
                models.Expense.expense_date
            ).label("month"),
            func.sum(
                models.Expense.amount
            ).label("total")
        )
        .filter(models.Expense.user_id == current_user)
        .group_by("month")
        .order_by("month")
        .all()
    )

    result = []

    for month, total in report:
        result.append({
            "month": int(month),
            "total_spent": total
        })

    return result