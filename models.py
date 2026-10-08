from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# URL базы данных (используем асинхронный SQLite для простоты локального запуска)
DATABASE_URL = "sqlite+aiosqlite:///./database.db"

# Создаем асинхронный engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Создаем объект Session на основе класса AsyncSession
# expire_on_commit=False предотвращает ошибки при обращении к объектам после коммита в асинхронном коде
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)

    # Связь с постами
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)

    # Связь с пользователем
    user = relationship("User", back_populates="posts")