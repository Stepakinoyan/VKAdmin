from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "level,founder,sphere,sort",
    [
        ("МО", "Козлов Александр Георгиевич", "Спорт", True),
        ("Регион", "Тимофеева Арина Артёмовна", "Культура", False),
        ("Ведомство", "Бочаров Егор Маркович", "Образование", False),
    ],
)
async def test_get_founder_by_level(
    level: str, founder: str, sphere: str, sort: bool, ac: AsyncClient
):
    response = await ac.get(
        "/filter/get_stats",
        params={"level": level, "founder": founder, "sphere": sphere, "sort": sort},
    )

    print(response.json())
    assert type(response.json()) == list
    assert response.status_code == 200
