from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectionBody(_message.Message):
    __slots__ = ["interface", "ip4info", "ip6info", "mac", "name", "uuid"]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    IP4INFO_FIELD_NUMBER: _ClassVar[int]
    IP6INFO_FIELD_NUMBER: _ClassVar[int]
    MAC_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    interface: _wrappers_pb2.StringValue
    ip4info: Netinfo
    ip6info: Netinfo
    mac: _wrappers_pb2.StringValue
    name: str
    uuid: str
    def __init__(self, name: _Optional[str] = ..., uuid: _Optional[str] = ..., interface: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., mac: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., ip4info: _Optional[_Union[Netinfo, _Mapping]] = ..., ip6info: _Optional[_Union[Netinfo, _Mapping]] = ...) -> None: ...

class ConnectionItem(_message.Message):
    __slots__ = ["id", "uuid"]
    ID_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    id: _wrappers_pb2.StringValue
    uuid: _wrappers_pb2.StringValue
    def __init__(self, id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., uuid: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class ConnectionReply(_message.Message):
    __slots__ = ["code", "data", "msg"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: int
    data: ConnectionBody
    msg: str
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., data: _Optional[_Union[ConnectionBody, _Mapping]] = ...) -> None: ...

class ConnectionUUIDRequest(_message.Message):
    __slots__ = ["uuid"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class ConnectionsReply(_message.Message):
    __slots__ = ["code", "data", "msg"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: int
    data: _containers.RepeatedCompositeFieldContainer[ConnectionBody]
    msg: str
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., data: _Optional[_Iterable[_Union[ConnectionBody, _Mapping]]] = ...) -> None: ...

class DevicesReply(_message.Message):
    __slots__ = ["code", "data", "msg"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: int
    data: _containers.RepeatedCompositeFieldContainer[DevicesReplyBody]
    msg: str
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., data: _Optional[_Iterable[_Union[DevicesReplyBody, _Mapping]]] = ...) -> None: ...

class DevicesReplyBody(_message.Message):
    __slots__ = ["conn", "conn_name", "connection", "dev_path", "device_type", "driver", "id_path", "ip4info", "ip6info", "is_managed", "mac", "name", "net_link_modes", "state", "virtual"]
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    CONN_FIELD_NUMBER: _ClassVar[int]
    CONN_NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEV_PATH_FIELD_NUMBER: _ClassVar[int]
    DRIVER_FIELD_NUMBER: _ClassVar[int]
    ID_PATH_FIELD_NUMBER: _ClassVar[int]
    IP4INFO_FIELD_NUMBER: _ClassVar[int]
    IP6INFO_FIELD_NUMBER: _ClassVar[int]
    IS_MANAGED_FIELD_NUMBER: _ClassVar[int]
    MAC_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NET_LINK_MODES_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_FIELD_NUMBER: _ClassVar[int]
    conn: _containers.RepeatedScalarFieldContainer[str]
    conn_name: _wrappers_pb2.StringValue
    connection: ConnectionItem
    dev_path: _wrappers_pb2.StringValue
    device_type: _wrappers_pb2.StringValue
    driver: _wrappers_pb2.StringValue
    id_path: _wrappers_pb2.StringValue
    ip4info: Netinfo
    ip6info: Netinfo
    is_managed: bool
    mac: str
    name: str
    net_link_modes: _containers.RepeatedScalarFieldContainer[str]
    state: str
    virtual: bool
    def __init__(self, conn: _Optional[_Iterable[str]] = ..., dev_path: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., device_type: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., id_path: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., ip4info: _Optional[_Union[Netinfo, _Mapping]] = ..., ip6info: _Optional[_Union[Netinfo, _Mapping]] = ..., is_managed: bool = ..., mac: _Optional[str] = ..., name: _Optional[str] = ..., state: _Optional[str] = ..., virtual: bool = ..., net_link_modes: _Optional[_Iterable[str]] = ..., conn_name: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., driver: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., connection: _Optional[_Union[ConnectionItem, _Mapping]] = ...) -> None: ...

class HostnameBody(_message.Message):
    __slots__ = ["hostname"]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    hostname: str
    def __init__(self, hostname: _Optional[str] = ...) -> None: ...

class HostnameReply(_message.Message):
    __slots__ = ["code", "data", "msg"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: int
    data: HostnameBody
    msg: str
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., data: _Optional[_Union[HostnameBody, _Mapping]] = ...) -> None: ...

class Netinfo(_message.Message):
    __slots__ = ["addresses", "dns", "gateway", "method", "routes"]
    ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    DNS_FIELD_NUMBER: _ClassVar[int]
    GATEWAY_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    addresses: _containers.RepeatedScalarFieldContainer[str]
    dns: _containers.RepeatedScalarFieldContainer[str]
    gateway: _wrappers_pb2.StringValue
    method: _wrappers_pb2.StringValue
    routes: _containers.RepeatedCompositeFieldContainer[Routes]
    def __init__(self, addresses: _Optional[_Iterable[str]] = ..., dns: _Optional[_Iterable[str]] = ..., gateway: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., method: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., routes: _Optional[_Iterable[_Union[Routes, _Mapping]]] = ...) -> None: ...

class NetworkingStateBody(_message.Message):
    __slots__ = ["state"]
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: bool
    def __init__(self, state: bool = ...) -> None: ...

class NetworkingStateReply(_message.Message):
    __slots__ = ["code", "data", "msg"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: int
    data: NetworkingStateBody
    msg: str
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., data: _Optional[_Union[NetworkingStateBody, _Mapping]] = ...) -> None: ...

class Routes(_message.Message):
    __slots__ = ["dest", "family", "metric", "next_hop"]
    DEST_FIELD_NUMBER: _ClassVar[int]
    FAMILY_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    NEXT_HOP_FIELD_NUMBER: _ClassVar[int]
    dest: str
    family: int
    metric: int
    next_hop: _wrappers_pb2.StringValue
    def __init__(self, dest: _Optional[str] = ..., family: _Optional[int] = ..., metric: _Optional[int] = ..., next_hop: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...
