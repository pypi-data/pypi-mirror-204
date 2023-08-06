import ipaddress
from typing import Any, List
from pydantic import BaseModel, Field


class ConfigOptions(BaseModel):
    activeBridge: bool
    authorized: bool
    capabilities: List[Any]
    ipAssignments: List[ipaddress.IPv4Address]
    noAutoAssignIps: bool
    tags: List[List[int]]


class ConfigRequest(BaseModel):
    hidden: bool
    name: str
    description: str
    config_options: ConfigOptions = Field(alias="config")


class Config(BaseModel):
    activeBridge: bool
    authorized: bool
    capabilities: List[Any]
    creationTime: int
    id: str
    identity: str
    ipAssignments: List[ipaddress.IPv4Address]
    lastAuthorizedTime: int
    lastDeauthorizedTime: int
    noAutoAssignIps: bool
    revision: int
    tags: List[List[int]]
    vMajor: int
    vMinor: int
    vRev: int
    vProto: int


class NetworkMember(BaseModel):
    id: str
    clock: int
    nettworkId: str
    nodeId: str
    controllerId: str
    hidden: bool
    name: str
    description: str
    config: Config
    lastOnline: int
    lastSeen: int
    physicalAddress: ipaddress.IPv4Address
    clientVersion: str
    protocolVersion: int
    supportsRulesEngine: bool
