from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.sql.models.base import Base


class SQLUser(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ref: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
