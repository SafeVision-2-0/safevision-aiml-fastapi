from sqlmodel import Field, Session, SQLModel, create_engine, select

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    image: str