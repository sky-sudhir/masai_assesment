from sqlalchemy import ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from api.db.db import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[int] = mapped_column(Integer, nullable=True)
    height: Mapped[int] = mapped_column(Integer, nullable=True)
    goals: Mapped[str] = mapped_column(String(100), nullable=True)



class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    plan_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    date: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    exercises: Mapped[str] = mapped_column(String(100), nullable=False)
    duration: Mapped[str] = mapped_column(String(100), nullable=False)


class Nutrition(Base):
    __tablename__ = "nutritions"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id: Mapped[int] = mapped_column(primary_key=True)
    plan_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    date: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    meals: Mapped[str] = mapped_column(String(100), nullable=False)


class Progress(Base):
    __tablename__ = "progress"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    workout_id: Mapped[int] = mapped_column(ForeignKey("workouts.id"))
    sets: Mapped[int] = mapped_column(Integer, nullable=False)
    reps: Mapped[int] = mapped_column(Integer, nullable=False)
    weights: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str] = mapped_column(String(100), nullable=False)















































