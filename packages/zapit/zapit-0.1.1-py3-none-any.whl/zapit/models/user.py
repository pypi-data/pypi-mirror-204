from typing import Dict, List, Optional
from pydantic import BaseModel


class LoginMethod(BaseModel):
    local: bool
    google: bool
    twitter: bool
    facebook: bool
    github: bool
    saml: bool
    oidc: bool


class UserUpdate(BaseModel):
    displayName: str


class User(BaseModel):
    id: str
    orgId: Optional[str] = None
    globalPermissions: Dict
    displayName: str
    email: str
    auth: Dict
    smsNumber: Optional[str] = None
    tokens: List


class Token(BaseModel):
    tokenName: str


class TokenRequest(Token):
    tokenName: str
    token: str
