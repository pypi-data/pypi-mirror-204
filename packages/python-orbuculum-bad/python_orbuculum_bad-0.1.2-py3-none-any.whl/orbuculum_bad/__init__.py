"""
This module is a subproject for orbuculum, it implentments the simplest function,
like get first network port or get the last network port for commerimal projects.
"""
from typing import Any, Dict, List
from grpc_requests import Client
from orbuculum_bad.protos.network import DevicesReplyBody

def get_all_ether_devices(client: Client) -> List[DevicesReplyBody]:
    """Get all devices from orbuculum grpc service

    Args:
        client: A grpc client instance.

    Returns:
        List of devices in form of grpc reply bodies.
    """
    devices = client.unary_unary(
            "network.Network", "ListDevices", {}, raw_output=True).data
    devices = sorted(devices, key=lambda x: x.connection.id.value)
    return list(filter(lambda x: x.device_type.value == "Ethernet", devices))


def filter_fibre_devices(devices: List[DevicesReplyBody]) -> List[DevicesReplyBody]:
    """Filter fibre devices via link modes of the device.

    Args:
        devices: List of devices in form of grpc reply bodies.

    Returns:
        List of devices with fibre mode in form of grpc reply bodies.
    """
    fibre_devices = []
    for device in devices:
        lower_net_link_modes = list(map(lambda x: x.lower(), device.net_link_modes))
        if "fiber" in lower_net_link_modes or "fibre" in lower_net_link_modes:
            fibre_devices.append(device)
    return fibre_devices


def filter_no_fibre_devices(devices: List[DevicesReplyBody]) -> List[DevicesReplyBody]:
    """Filter none fibre devices via link modes of the device.

    Args:
        devices: List of devices in form of grpc reply bodies.

    Returns:
        List of devices without fibre mode in form of grpc reply bodies.
    """
    no_fibre_devices = []
    for device in devices:
        lower_net_link_modes = list(map(lambda x: x.lower(), device.net_link_modes))
        if "fiber" not in lower_net_link_modes and "fibre" not in lower_net_link_modes:
            no_fibre_devices.append(device)
    return no_fibre_devices


class OrbuculumEtherClient(object):
    """The client for Orbuculum service

    A client which handles ethernet devices with the order from orbuculum.

    Args:
        url: The url for the orbuculum grpc server.

    Attributes:
        client: The grpc client for orbuculum grpc server.
        devices: List of devices in form of grpc reply bodies.
        fibre_devices: List of devices with fibre mode in form of grpc reply bodies.
        no_fibre_devices: List of devices without fibre mode in form of grpc reply bodies.
    """
    def __init__(self, url: str) -> None:
        self.client = Client(url)
        self.devices: List[DevicesReplyBody] = get_all_ether_devices(self.client)
        self.fibre_devices = filter_fibre_devices(self.devices)
        self.no_fibre_devices = filter_no_fibre_devices(self.devices)

    def get_first_port(self) -> str:
        """Retrive the first network card.

        Returns:
            The interface name of the first network card.
            If there're no interface names, returns an empty string.
        """
        if len(self.devices) > 0:
            return self.devices[0].name
        return ''

    def get_last_port(self) -> str:
        """Retrive the last network card.

        Returns:
            The interface name of the last network card.
            If there're no interface names, returns an empty string.
        """
        if len(self.devices) > 0:
            return self.devices[-1].name
        return ''

    def get_first_fibre_port(self) -> str:
        """Retrive the first network card with fibre linkmode.

        Returns:
            The interface name of the first network card with fibre linkmode.
            If there're no interfaces with fibre linkmode, returns an empty string.
        """
        if len(self.fibre_devices) > 0:
            return self.fibre_devices[0].name
        return ''

    def get_last_fibre_port(self) -> str:
        """Retrive the last network card with fibre linkmode.

        Returns:
            The interface name of the last network card with fibre linkmode.
            If there're no interfaces with fibre linkmode, returns an empty string.
        """
        if len(self.fibre_devices) > 0:
            return self.fibre_devices[-1].name
        return ''

    def get_first_no_fibre_port(self) -> str:
        """Retrive the first network card without fibre linkmode.

        Returns:
            The interface name of the first network card without fibre linkmode.
            If there're no interfaces without fibre linkmode, returns an empty string.
        """
        if len(self.no_fibre_devices) > 0:
            return self.no_fibre_devices[0].name
        return ''

    def get_last_no_fibre_port(self) -> str:
        """Retrive the last network card without fibre linkmode.

        Returns:
            The interface name of the last network card without fibre linkmode.
            If there're no interfaces without fibre linkmode, returns an empty string.
        """
        if len(self.no_fibre_devices) > 0:
            return self.no_fibre_devices[-1].name
        return ''

    def get_connection_mapping(self) -> Dict[str, str]:
        """Retrive connection names' mapping.

        Returns:
            The mapping of connection names to interfaces.
        """
        mapping = {}
        for device in self.devices:
            mapping[device.connection.id.value] = device.name
        return mapping

    def get_interface_mapping(self) -> Dict[str, str]:
        """Retrive interfaces' mapping.

        Returns:
            The mapping of interfaces to connection names.
        """
        mapping = {}
        for device in self.devices:
            mapping[device.name] = device.connection.id.value
        return mapping

    def get_all_ip_addresses(self) -> List[str]:
        """retrive all ip addresses from all the ethernet devices

        Returns:
            List of ip addresses, including ipv4 or ipv6.
        """
        ipaddrs = []
        for device in self.devices:
            ipaddrs.extend(list(device.ip4info.addresses))
        for device in self.devices:
            ipaddrs.extend(list(device.ip6info.addresses))
        return ipaddrs
