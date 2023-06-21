from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship

from app.globals import db, ma

from app.modules.user.model import User


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = Column(Integer, primary_key=True)
    author_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))
    created_at: Mapped[datetime] = Column(DateTime)
    title: Mapped[str] = Column(String, nullable=False)
    body: Mapped[str] = Column(Text)

    author: Mapped["User"] = relationship("User", back_populates="posts")


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
