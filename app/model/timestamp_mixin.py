from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Annotated


# 現在時刻を返す関数（デフォルト値として使用）
def now_utc() -> datetime:
    return datetime.now()


# タイムスタンプ用の型エイリアス
TimestampColumn = Annotated[datetime, mapped_column(nullable=False)]


class TimestampMixin:
    created_at: Mapped[TimestampColumn] = mapped_column(default=now_utc)
    updated_at: Mapped[TimestampColumn] = mapped_column(
        default=now_utc, onupdate=now_utc
    )
