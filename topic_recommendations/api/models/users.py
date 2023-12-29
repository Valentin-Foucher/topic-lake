from pydantic import BaseModel


class CreateUserModel(BaseModel):
    name: str
    password: str


class User(BaseModel):
    id: int
    name: str


class GetUser(BaseModel):
    user: User
