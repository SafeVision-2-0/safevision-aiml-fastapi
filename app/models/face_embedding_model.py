from sqlmodel import Field, SQLModel

class FaceEmbedding(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_image_id: int = Field(foreign_key="userimage.id")
    vector: str