from enum import Enum
from typing import List
from pydantic import BaseModel

from zapit.models.network import SSOConfig


class InvitationRequest(BaseModel):
    email: str


class InvitationStatus(str, Enum):
    PENDING = "pending"
    ACCPETED = "accepted"
    CANCELED = "canceled"


class Invitation(BaseModel):
    orgId: str
    email: str
    id: str
    creation_time: int
    status: InvitationStatus
    update_time: int
    ownerEmail: str


class Member(BaseModel):
    orgId: str
    userId: str
    name: str
    email: str


class Organization(BaseModel):
    id: str
    ownerId: str
    ownerEmail: str
    members: List[Member]
    ssoConfig: SSOConfig
