from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.models.profile_model import Profile
    from app.models.face_embedding_model import FaceEmbedding

class ProfileImage(SQLModel, table=True):
    __tablename__ = "profile_image"
    
    id: int | None = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profile.id")
    image_path: str
    
    profile: "Profile" = Relationship(back_populates="images")
    embeddings: List["FaceEmbedding"] = Relationship(back_populates="profile_image")