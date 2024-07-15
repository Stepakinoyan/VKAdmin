from app.auth.models import Users
from app.dao.dao import BaseDAO


class UserDAO(BaseDAO):
    model = Users
