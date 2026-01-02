from sqlmodel import Field, SQLModel
from sqlalchemy import Column, JSON

class FaceEmbedding(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_image_id: int = Field(foreign_key="userimage.id")
    vector: list[float] = Field(sa_column=Column(JSON))