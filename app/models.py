from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey
)

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    amount = Column(Float, nullable=False)

    category = Column(String, nullable=False)

    description = Column(String, nullable=True)

    expense_date = Column(Date, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    month = Column(
        String,
        nullable=False
    )

    year = Column(
        Integer,
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )