from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from planner.auth.hash_password import HashPassword
from planner.auth.jwt_handler import create_access_token
from planner.database.connection import Database
from planner.models.users import User, TokenResponse

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


@users_router.post('/signin', response_model=TokenResponse)
async def signin(user: OAuth2PasswordRequestForm = Depends()):
    user_exist = await User.find_one(User.email == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Email not registered'
        )
    if not hash_password.verify_password(user.password, user_exist.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Password mismatch'
        )

    access_token = create_access_token(user_exist.email)
    return {
        'access_token': access_token,
        'token_type': 'Bearer'
    }
