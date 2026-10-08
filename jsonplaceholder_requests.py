import aiohttp

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_json(session: aiohttp.ClientSession, url: str) -> list[dict]:
    """Базовая асинхронная функция для получения JSON-данных."""
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()


async def fetch_users_data() -> list[dict]:
    """Получает список пользователей с API."""
    async with aiohttp.ClientSession() as session:
        return await fetch_json(session, USERS_DATA_URL)


async def fetch_posts_data() -> list[dict]:
    """Получает список постов с API."""
    async with aiohttp.ClientSession() as session:
        return await fetch_json(session, POSTS_DATA_URL)