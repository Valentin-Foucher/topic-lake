from pydantic import BaseModel


class CreateUserModel(BaseModel):
    name: str
    password: str
