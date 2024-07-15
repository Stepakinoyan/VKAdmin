from httpx import AsyncClient


async def test_get_all_stats(ac: AsyncClient):
    response = await ac.get("/filter/get_all_stats")

    data = response.json()

    print(data)
    assert isinstance(data, list)
    assert response.status_code == 200
