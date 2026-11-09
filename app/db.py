from pathlib import Path
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import get_settings

class Base(DeclarativeBase): pass
url = get_settings().database_url
if url.startswith("sqlite:///"):
    path = url[len("sqlite:///"):]
    if path != ":memory:": Path(path).parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def initialize_database():
    Base.metadata.create_all(bind=engine)
    # Lightweight forward migration for databases created by the earlier v2 schema.
    if engine.dialect.name == "sqlite" and inspect(engine).has_table("jobs"):
        columns = {column["name"] for column in inspect(engine).get_columns("jobs")}
        if "error" not in columns:
            with engine.begin() as connection:
                connection.execute(text("ALTER TABLE jobs ADD COLUMN error TEXT"))

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
