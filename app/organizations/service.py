from fastapi.encoders import jsonable_encoder
from app.organizations.dao import OrganizationsDAO


class OrganizationsService:
    async def filter_channels(self, **args):
        organizations = await OrganizationsDAO.filter_channels(**args)
        return jsonable_encoder(organizations)


service = OrganizationsService()
