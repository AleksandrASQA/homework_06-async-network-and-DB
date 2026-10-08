import asyncio
from models import Base, engine, Session, User, Post
from jsonplaceholder_requests import fetch_users_data, fetch_posts_data


async def create_tables() -> None:
    """Асинхронное создание таблиц в базе данных."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def save_data_to_db(users_data: list[dict], posts_data: list[dict]) -> None:
    """Асинхронное сохранение полученных данных в базу данных."""
    async with Session() as session:
        # Создаем объекты пользователей из словарей
        users = [
            User(
                id=user["id"],
                name=user["name"],
                username=user["username"],
                email=user["email"]
            )
            for user in users_data
        ]

        # Создаем объекты постов из словарей
        posts = [
            Post(
                id=post["id"],
                user_id=post["userId"],
                title=post["title"],
                body=post["body"]
            )
            for post in posts_data
        ]

        # Используем merge для обновления или создания записей
        for user in users:
            await session.merge(user)

        for post in posts:
            await session.merge(post)

        # Фиксируем изменения в БД
        await session.commit()


async def async_main() -> None:
    """Основной асинхронный цикл программы."""
    # 1. Создание таблиц (инициализация)
    await create_tables()
    
    # 2. Загрузка пользователей и постов конкурентно (параллельно)
    users_data, posts_data = await asyncio.gather(
        fetch_users_data(),
        fetch_posts_data(),
    )
    
    # 3. Добавление пользователей и постов в базу данных
    await save_data_to_db(users_data, posts_data)
    
    # 4. Закрытие соединения с БД
    await engine.dispose()


def main() -> None:
    """Точка входа в программу."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()