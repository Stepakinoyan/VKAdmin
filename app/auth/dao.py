from app.dao.dao import BaseDAO
from app.auth.model import Users

class UserDAO(BaseDAO):
    model = Users