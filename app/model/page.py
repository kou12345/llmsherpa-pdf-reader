from sqlalchemy import ForeignKey, Index, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from model.timestamp_mixin import TimestampMixin
from database import Base


class Page(Base, TimestampMixin):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", ondelete="CASCADE"), nullable=False
    )
    page_number: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text)
    book: Mapped["Book"] = relationship(back_populates="pages")  # type: ignore

    __table_args__ = (
        Index("ix_pages_content_pgroonga", "content", postgresql_using="pgroonga"),
    )
