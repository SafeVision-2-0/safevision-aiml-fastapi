from sqlmodel import Session, create_engine
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=True, # Melihat query SQL
    pool_pre_ping=True
)

def get_session():
    """
    Dependency FastAPI untuk mendapatkan DB session.
    Session akan otomatis ditutup setelah request selesai.
    """
    with Session(engine) as session:
        yield session