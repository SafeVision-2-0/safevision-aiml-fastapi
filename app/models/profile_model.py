from sqlmodel import Field, SQLModel, Relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.profile_image_model import ProfileImage

class Profile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    
    images: list["ProfileImage"] = Relationship(back_populates="profile")