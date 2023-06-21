from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

# from marshmallow import fields

from app.globals import db, ma


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = Column(Integer, primary_key=True)
    author_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))
    created_at: Mapped[datetime] = Column(DateTime, server_default=func.now())
    title: Mapped[str] = Column(String, nullable=False)
    body: Mapped[str] = Column(Text)

    author: Mapped["User"] = relationship("User", back_populates="posts")


from app.modules.user.model import User  # noqa


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True

    # author = fields.Nested(UserSchema)
