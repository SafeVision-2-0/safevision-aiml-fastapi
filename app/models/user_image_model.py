from sqlmodel import Field, SQLModel, Relationship
from app.models.user_model import User

class UserImage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    image_path: str
    
    user: "User" = Relationship(back_populates="images")