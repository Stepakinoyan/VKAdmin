import httpx
from faststream.nats import NatsBroker
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_faststream import BrokerWrapper, StreamScheduler

from app.config import settings

broker = NatsBroker(servers="nats://nats:4222")


@broker.subscriber("get-stats")
async def handler():
    async with httpx.AsyncClient() as client:
        get_gos_bage = await client.post(
            f"http://{settings.DOMAIN}/api/vk/get_gos_bage", timeout=6000
        )
        print(f"/vk/get_gos_bage: {get_gos_bage.status_code}")

        wall_get_all = await client.post(
            f"http://{settings.DOMAIN}/api/vk/wall_get_all", timeout=6000
        )
        print(f"/vk/wall_get_all: {wall_get_all.status_code}")

        wall_get_all = await client.post(
            f"http://{settings.DOMAIN}/api/vk/get_group_data", timeout=6000
        )
        print(f"/vk/wall_get_all: {wall_get_all.status_code}")

        get_weekly_audience_reach = await client.post(
            f"http://{settings.DOMAIN}/api/vk/get_weekly_audience_reach", timeout=6000
        )
        print(f"/vk/get_weekly_audience_reach: {get_weekly_audience_reach.status_code}")

        wall_get_all = await client.post(
            f"http://{settings.DOMAIN}/api/vk/get_views", timeout=6000
        )
        print(f"/vk/wall_get_all: {wall_get_all.status_code}")

        get_stat = await client.post(
            f"http://{settings.DOMAIN}/api/vk/get_stat", timeout=6000
        )
        print(f"/vk/get_stat: {get_stat.status_code}")


taskiq_broker = BrokerWrapper(broker)

taskiq_broker.task(
    subject="get-stats",
    schedule=[{"cron": "0 0 * * *", "cron_offset": "Asia/Yakutsk"}],
)

scheduler = StreamScheduler(
    broker=taskiq_broker,
    sources=[LabelScheduleSource(taskiq_broker)],
)
