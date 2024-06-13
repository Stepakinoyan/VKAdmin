import httpx
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend
from app.config import settings

redis_async_result = RedisAsyncResultBackend(
    redis_url=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
)

broker = ListQueueBroker(
    url=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
).with_result_backend(redis_async_result)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


@broker.task(schedule=[{"cron": "0 0 * * *", "cron_offset": "Asia/Yakutsk"}])
async def send_requests() -> None:
    async with httpx.AsyncClient() as client:
        try:
            get_gos_bage = await client.get(
                "http://api:8000/vk/get_gos_bage", timeout=60000
            )
            print(f"/vk/get_gos_bage: {get_gos_bage.status_code}")

            wall_get_all = await client.get(
                "http://api:8000/vk/wall_get_all", timeout=60000
            )
            print(f"/vk/wall_get_all: {wall_get_all.status_code}")

            get_stat = await client.get("http://api:8000/vk/get_stat", timeout=60000)
            print(f"/vk/get_stat: {get_stat.status_code}")

        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
