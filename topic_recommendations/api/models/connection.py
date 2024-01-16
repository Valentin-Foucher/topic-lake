from pydantic import BaseModel


class LogInRequest(BaseModel):
    username: str
    password: str


class LogInResponse(BaseModel):
    token: str


class LogOutRequest(BaseModel):
    user_id: int
