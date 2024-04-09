from app.dao.dao import BaseDAO
from app.auth.models import Users


class UserDAO(BaseDAO):
    model = Users
