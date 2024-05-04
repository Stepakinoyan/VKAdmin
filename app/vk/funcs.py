from sqlalchemy import select
import httpx
from openpyxl import Workbook
import redis.asyncio as redis
import asyncio
from rich.console import Console
from app.config import settings
from app.database import get_session
from app.vk.models import Account
from sqlalchemy.ext.asyncio import AsyncSession

redis_ = redis.from_url(
    f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    encoding="utf-8",
    decode_responses=True,
    socket_timeout=5,
    socket_keepalive=True,
)
console = Console(color_system="truecolor", width=140)


async def call(method: str, params: dict, access_token: str, retries: int = 3):
    base_url = "https://api.vk.com/method/"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept-Language": "ru-RU,ru;q=0.9",
    }

    params["v"] = "5.217"

    async with httpx.AsyncClient(timeout=30.0, http2=True) as client:
        for _ in range(retries):  # Пытаемся выполнить запрос retries раз
            if retries < 3:
                console.rule(f"retries {retries}")
            response = await client.post(
                f"{base_url}{method}", params=params, headers=headers
            )

            # print(response.status_code)

            if response.status_code in [400, 403, 404, 500, 502]:
                console.rule(f"[red] ERROR {response.status_code}")
                return {"error": response.status_code}

            response_data = response.json()
            # Проверяем, содержит ли ответ ошибку "Too many requests per second"
            if (
                "error" in response_data
                and response_data["error"].get("error_code") == 6
            ):
                console.rule(f"[red] {response.url} Too many requests per second")
                # Если да, делаем паузу и пробуем ещё раз
                await asyncio.sleep(20)
            else:
                # Если нет ошибки, или это была последняя попытка, возвращаем результат
                return response_data
        return {"error": "Max retries exceeded"}


def load_vk_links(file_path: str) -> list:
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Remove any trailing or leading whitespace from each line
    lines = [line.strip() for line in lines]

    # Split the list into chunks of 500 items each
    chunks = [lines[i:i + 500] for i in range(0, len(lines), 500)]

    return chunks


async def fetch_gos_page(url, account_id):
    headers = {
        "Accept-Language": "ru-RU,ru;q=0.9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200 and 'GovernmentCommunityBadge' in response.text:
            print(f"{account_id}: {url}")
            return account_id
        elif response.status_code in [400, 401, 403, 500]:
            print(f"[{response.status_code}] {account_id}: {url}")
    return None

async def save_accounts_to_xlsx(file_path: str, session: AsyncSession):
    # 1. Fetch all data from the accounts table
    result = await session.execute(select(Account))
    accounts = result.scalars().all() 

    # 2. Create a new XLSX workbook and sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Accounts"

    # Set headers for the sheet
    headers = [
        "id", "screen_name", "type", "name", "city", "activity", "verified",
        "has_avatar", "has_cover", "has_description", "has_gos_badge",
        "has_widget", "widget_count", "members_count", "site", "date_added",
        "posts", "posts_1d", "posts_7d", "posts_30d", "post_date"
    ]
    ws.append(headers)

    # Append account data to the sheet
    for account in accounts:
        ws.append([
            account.id, account.screen_name, account.type, account.name,
            account.city, account.activity, account.verified, account.has_avatar,
            account.has_cover, account.has_description, account.has_gos_badge,
            account.has_widget, account.widget_count, account.members_count,
            account.site, account.date_added, account.posts, account.posts_1d,
            account.posts_7d, account.posts_30d, account.post_date
        ])

    # Save the workbook to the specified file path
    wb.save(file_path)