from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger

from database.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)