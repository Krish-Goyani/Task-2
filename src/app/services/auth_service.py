from src.app.model.schemas.user_schemas import UserIn
from src.app.repositories.user_repository import UserRepository
from src.app.utils.security import get_hashed_password, verify_password, create_access_token
from fastapi import Depends, HTTPException
from src.app.config.database import mongodb_database


class AuthService:
    def __init__(self, auth_collection=Depends(mongodb_database.get_auth_collection), user_repository=Depends(UserRepository)) -> None:
        self.auth_collection = auth_collection
        self.user_repository = user_repository

    async def register_user_service(self, userdata: UserIn):
        if not userdata:
            raise HTTPException(status_code=400, detail="User data is required")

        # Check if the user already exists
        user = await self.user_repository.find_user_by_email(userdata.email, self.auth_collection)
        if user:
            raise HTTPException(status_code=409, detail="User with this email already exists")

        data = userdata.model_dump()
        data["password_hash"] = get_hashed_password(data["password"])

        # Attempt to insert the new user
        insertion_result = await self.user_repository.insert_user(data, self.auth_collection)
        if not insertion_result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to register user")
        
        return str(insertion_result.inserted_id)

    async def login_user_service(self, form_data):
        if not form_data or not form_data.username or not form_data.password:
            raise HTTPException(status_code=400, detail="Username and password are required")

        # Fetch user by email
        user = await self.user_repository.find_user_by_email(form_data.username, self.auth_collection)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Verify the password
        hashed_pass = user["password_hash"]
        if not verify_password(form_data.password, hashed_pass):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Create access and refresh tokens
        access_token = create_access_token(user['email'])

        return {
            "access_token": access_token,
        }

    async def get_all_users(self):
        users = await self.user_repository.get_all_users(self.auth_collection)
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        return users

    async def update_user_role(self, user_id, new_role):
        if not user_id or not new_role:
            raise HTTPException(status_code=400, detail="User ID and new role are required")

        update_result = await self.user_repository.update_user_role(user_id, new_role, self.auth_collection)
        return {"message": "User role updated successfully"}
