from httpx import AsyncClient


async def test_get_all_stats(ac: AsyncClient):
    response = await ac.get("/filter/get_all_stats")

    print(response.json())
    assert type(response.json()) == list
    assert response.status_code == 200
