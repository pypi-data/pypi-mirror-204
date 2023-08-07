import typing
from datetime import datetime
from enum import Enum

from nacos.models import BaseModel


class AccessToken(BaseModel):
    accessToken: str
    tokenTtl: int


class NacosBaseModel(BaseModel):
    code: int
    message: typing.Optional[str]
    data: typing.Union[dict, list, bool]


class MetaDataModel(BaseModel):
    value: str


class InstanceModel(BaseModel):
    '''Instance'''
    serviceName: typing.Optional[str]
    service: typing.Union[str, None]
    ip: str
    port: int
    clusterName: str
    weight: float
    healthy: bool
    enabled: typing.Optional[bool]
    ephemeral: typing.Optional[bool]
    instanceId: typing.Optional[str]
    instanceHeartBeatInterval: typing.Optional[int]
    instanceIdGenerator: typing.Optional[str]
    instanceHeartBeatTimeOut: typing.Optional[int]
    ipDeleteTimeout: typing.Optional[int]
    metadata: typing.Union[MetaDataModel, dict]


class InstanceListModel(BaseModel):
    '''Instance list'''
    name: str
    groupName: str
    clusters: str
    cacheMillis: int
    lastRefTime: int
    checksum: str
    allIPs: bool
    reachProtectionThreshold: bool
    valid: bool
    hosts: typing.List[InstanceModel]


class InstanceSendHeartBeatModel(BaseModel):
    ''' Instance send heartbeat'''
    clientBeatInterval: int
    code: int
    lightBeatEnabled: bool


class ServiceListDataModel(BaseModel):
    count: int
    services: typing.List[str]


class ServiceListModel(NacosBaseModel):
    data: typing.Union[ServiceListDataModel, dict]


class ServiceInfoModel(BaseModel):
    namespaceId: str
    groupName: str
    name: str
    protectThreshold: float
    metadata: dict
    selector: dict
    clusters: typing.List[dict]
