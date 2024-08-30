from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.timestamp_mixin import TimestampMixin
from database import Base


class Book(Base, TimestampMixin):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    pages: Mapped[List["Page"]] = relationship(  # type: ignore
        back_populates="book", cascade="all, delete-orphan"
    )
