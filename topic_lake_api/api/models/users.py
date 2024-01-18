from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    password: str


class CreateUserResponse(BaseModel):
    id: int


class User(BaseModel):
    id: int
    name: str


class GetUserResponse(BaseModel):
    user: User


