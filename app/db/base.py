from app.models import User, Task  # noqa: F401
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass