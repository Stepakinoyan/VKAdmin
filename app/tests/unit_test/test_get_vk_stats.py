from httpx import AsyncClient
    
async def test_get_vk_stats(ac: AsyncClient):
    response = await ac.get(
        "/vk/get_stat"
    )

    print(response.json())
    assert response.status_code == 200
