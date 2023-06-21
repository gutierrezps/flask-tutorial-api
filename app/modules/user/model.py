from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app import db, ma


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String(50), unique=True, nullable=False)
    password: Mapped[str] = Column(String, nullable=False)

    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates="author")


from app.modules.post.model import Post  # noqa: E402


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ("password",)
