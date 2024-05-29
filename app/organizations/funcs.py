from app.organizations.schemas import Sphere


def get_unique_spheres(items: list[Sphere]) -> list[Sphere]:
    """

    Возвращает список уникальных объектов типа Sphere.

    """

    spheres = []
    for item in list(set(filter(lambda item: item is not None, items))):
        spheres.append({"sphere": item})

    return spheres
