from faststream.nats import NatsBroker
import httpx
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_faststream import BrokerWrapper, StreamScheduler


broker = NatsBroker(servers="nats://nats:4222")


@broker.subscriber("get-stats")
async def handler():
    async with httpx.AsyncClient() as client:
        try:
            get_gos_bage = await client.post(
                "http://api:8000/vk/get_gos_bage", timeout=6000
            )
            print(f"/vk/get_gos_bage: {get_gos_bage.status_code}")

            wall_get_all = await client.post(
                "http://api:8000/vk/wall_get_all", timeout=6000
            )
            print(f"/vk/wall_get_all: {wall_get_all.status_code}")

            get_stat = await client.post("http://api:8000/vk/get_stat", timeout=6000)
            print(f"/vk/get_stat: {get_stat.status_code}")

        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


taskiq_broker = BrokerWrapper(broker)

taskiq_broker.task(
    subject="get-stats",
    schedule=[{"cron": "0 0 * * *", "cron_offset": "Asia/Yakutsk"}],
)

scheduler = StreamScheduler(
    broker=taskiq_broker,
    sources=[LabelScheduleSource(taskiq_broker)],
)
