import pytest
from sqlalchemy import select
from models import Session, User, Post
from jsonplaceholder_requests import fetch_users_data, fetch_posts_data
from main import async_main


@pytest.mark.asyncio
async def test_fetch_users_data():
    """Тест получения данных пользователей с API."""
    users_data = await fetch_users_data()
    assert isinstance(users_data, list)
    assert len(users_data) > 0
    assert "id" in users_data[0] and "name" in users_data[0]


@pytest.mark.asyncio
async def test_fetch_posts_data():
    """Тест получения данных постов с API."""
    posts_data = await fetch_posts_data()
    assert isinstance(posts_data, list)
    assert len(posts_data) > 0
    assert "id" in posts_data[0] and "userId" in posts_data[0]


@pytest.mark.asyncio
async def test_full_cycle_and_relationships():
    """
    Комплексный тест:
    1. Запускает полный цикл (async_main)
    2. Проверяет наличие данных в БД
    3. Проверяет связи (relationship) между User и Post
    """
    from sqlalchemy.orm import selectinload

    # 1. Запускаем основную асинхронную функцию
    await async_main()

    # 2. Проверяем данные в БД с явной загрузкой связей
    async with Session() as session:
        # Загружаем пользователей с постами (чтобы избежать lazy loading после dispose)
        users_result = await session.execute(
            select(User).options(selectinload(User.posts))
        )
        users = users_result.scalars().unique().all()

        assert len(users) > 0, "Пользователи не были сохранены в БД"

        # Проверяем посты отдельно
        posts_result = await session.execute(select(Post))
        posts = posts_result.scalars().all()
        assert len(posts) > 0, "Посты не были сохранены в БД"

        # 3. Проверяем связи (relationship)
        first_user = users[0]

        # Проверяем, что у него есть атрибут posts (связь User -> Post)
        assert hasattr(first_user, 'posts'), "У модели User нет связи posts"
        assert isinstance(first_user.posts, list), "Связь posts должна быть списком"

        if len(first_user.posts) > 0:
            first_post = first_user.posts[0]
            # Проверяем обратную связь (Post -> User)
            assert hasattr(first_post, 'user'), "У модели Post нет связи user"
            assert first_post.user is not None, "Связь user не должна быть None"
            assert first_post.user.id == first_user.id, "ID пользователя в посте не совпадает"