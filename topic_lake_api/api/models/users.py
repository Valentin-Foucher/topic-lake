from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=4, max_length=64)
    password: str = Field(min_length=8, max_length=64)


class CreateUserResponse(BaseModel):
    id: int


class User(BaseModel):
    id: int
    name: str


class GetUserResponse(BaseModel):
    user: User


