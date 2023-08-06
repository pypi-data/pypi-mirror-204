from pydantic import BaseModel

from zapit.models.user import LoginMethod, User


class Status(BaseModel):
    id: str
    type: str
    clock: int
    version: str
    apiVersion: str
    uptime: int
    user: User
    readOnlyMode: bool
    loginMethods: LoginMethod


class RandomToken(BaseModel):
    clock: int
    raw: str
    token: str
