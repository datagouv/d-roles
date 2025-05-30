# ------- REPOSITORY FILE -------
from ..models import UserCreate, UserResponse, UserWithRoleResponse


class UsersRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    async def get_user_by_email(self, email: str) -> UserResponse:
        async with self.db_session.transaction():
            query = """
            SELECT * FROM users as U WHERE U.email = :email
            """
            return await self.db_session.fetch_one(query, {"email": email})

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        async with self.db_session.transaction():
            query = """
            SELECT * FROM users as U WHERE U.id = :id
            """
            return await self.db_session.fetch_one(query, {"id": user_id})

    async def get_users_by_group_id(self, group_id: int) -> list[UserWithRoleResponse]:
        async with self.db_session.transaction():
            query = """
                SELECT U.id, U.email, U.sub_pro_connect, U.created_at, R.role_name, R.is_admin
                FROM users as U
                INNER JOIN group_user_relations as TUR ON TUR.user_id = U.id
                INNER JOIN roles as R ON TUR.role_id = R.id
                WHERE TUR.group_id = :group_id
                """
            return await self.db_session.fetch_all(query, {"group_id": group_id})

    async def add_user(self, user: UserCreate) -> UserResponse:
        async with self.db_session.transaction():
            query = "INSERT INTO users (email, is_email_confirmed) VALUES (:email, :is_email_confirmed) RETURNING *"
            values = {"email": user.email, "is_email_confirmed": False}
            return await self.db_session.fetch_one(query, values)
