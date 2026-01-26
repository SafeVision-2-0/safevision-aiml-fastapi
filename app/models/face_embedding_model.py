from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, JSON
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.profile_image_model import ProfileImage

class FaceEmbedding(SQLModel, table=True):
    __tablename__ = "face_embedding"
    
    id: int | None = Field(default=None, primary_key=True)
    profile_image_id: int = Field(foreign_key="profile_image.id")
    vector_casia: list[float] = Field(sa_column=Column(JSON))
    vector_vgg: list[float] = Field(sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    profile_image: "ProfileImage" = Relationship(back_populates="embeddings")