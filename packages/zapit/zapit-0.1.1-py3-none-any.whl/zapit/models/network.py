import ipaddress
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class V4AssignMode(BaseModel):
    zt: bool


class V6AssignMode(BaseModel):
    zt: bool
    NDP6plane: bool = Field(alias="6plane")
    rfc4193: bool


class DNS(BaseModel):
    domain: Optional[str] = None
    servers: Optional[List[ipaddress.IPv4Address]] = None


class SSOConfig(BaseModel):
    enabled: bool
    mode: Optional[str] = None
    clientId: Optional[str] = None
    issuer: Optional[str] = None
    provider: Optional[str] = None
    authorizationEndpoint: Optional[str] = None
    allowList: Optional[List[Any]] = None


class Via(BaseModel):
    target: str


class Route(BaseModel):
    target: ipaddress.IPv4Network
    via: Optional[Via] = None


class AssignmentPool(BaseModel):
    ipRangeStart: ipaddress.IPv4Address
    ipRangeEnd: ipaddress.IPv4Address


class Config(BaseModel):
    id: str
    creationTime: int
    capabilities: List[Any]
    dns: DNS
    enableBroadcast: bool
    ipAssignmentPools: Optional[List[Any]] = None
    lastModified: int
    mtu: int
    multicastLimit: int
    name: str
    private: bool
    routes: List[Route]
    rules: List[Any]
    ssoConfig: SSOConfig
    tags: List[Any]
    v4AssignMode: V4AssignMode
    v6AssignMode: V6AssignMode


class Permissions(BaseModel):
    a: bool
    d: bool
    m: bool
    r: bool


class ConfigNetwork(BaseModel):
    config: Config
    description: str
    rulesSource: str
    permissions: Optional[Dict[str, Permissions]] = None
    ownerId: str
    capabilitiesByName: Dict
    tagsByName: Dict


class Network(ConfigNetwork):
    id: str
    clock: int
    onlineMemberCount: int
    authorizedMemberCount: int
    totalMemberCount: int
