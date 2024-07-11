from fastapi import APIRouter, HTTPException, status

from planner.auth.hash_password import HashPassword
from planner.database.connection import Database
from planner.models.users import User, UserSingIn

users_router = APIRouter(
    tags=['User']
)

users = {}

user_database = Database(User)
hash_password = HashPassword()


@users_router.post('/signup')
async def signup(user: User):
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Email already registered'
        )

    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    await user_database.save(user)
    return {
        'message': 'User registered',
    }


@users_router.post('/signin')
async def signin(user: UserSingIn):
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Email not registered'
        )
    if user_exist.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Password mismatch'
        )

    return {
        'message': 'User signed in successfully',
    }
