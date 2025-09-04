from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import crud_user
from app.schemas.user import UserCreate

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_data: dict):
        """
        Service layer to create a user.
        This is where business logic would go.
        For now, it just calls the CRUD function.
        """
        # In a real app, you might have more logic here,
        # like sending a welcome email, etc.
        user_create_schema = UserCreate(**user_data)
        user = await crud_user.user.create(db=self.session, obj_in=user_create_schema)
        return user
