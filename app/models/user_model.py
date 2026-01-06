from sqlmodel import Field, SQLModel, Relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user_image_model import UserImage

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    images: list["UserImage"] = Relationship(back_populates="user")