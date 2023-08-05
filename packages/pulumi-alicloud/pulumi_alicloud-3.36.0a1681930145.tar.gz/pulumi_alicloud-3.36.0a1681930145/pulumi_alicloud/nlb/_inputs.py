# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'LoadBalancerZoneMappingArgs',
    'ServerGroupHealthCheckArgs',
]

@pulumi.input_type
class LoadBalancerZoneMappingArgs:
    def __init__(__self__, *,
                 vswitch_id: pulumi.Input[str],
                 zone_id: pulumi.Input[str],
                 allocation_id: Optional[pulumi.Input[str]] = None,
                 eni_id: Optional[pulumi.Input[str]] = None,
                 ipv6_address: Optional[pulumi.Input[str]] = None,
                 private_ipv4_address: Optional[pulumi.Input[str]] = None,
                 public_ipv4_address: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] vswitch_id: The vSwitch in the zone. You can specify only one vSwitch (subnet) in each zone of an NLB instance.
        :param pulumi.Input[str] zone_id: The ID of the zone of the NLB instance.
        :param pulumi.Input[str] allocation_id: The ID of the EIP associated with the Internet-facing NLB instance.
        :param pulumi.Input[str] eni_id: The ID of the elastic network interface (ENI).
        :param pulumi.Input[str] ipv6_address: The IPv6 address of the NLB instance.
        :param pulumi.Input[str] private_ipv4_address: The private IPv4 address of the NLB instance.
        :param pulumi.Input[str] public_ipv4_address: The public IPv4 address of the NLB instance.
        """
        pulumi.set(__self__, "vswitch_id", vswitch_id)
        pulumi.set(__self__, "zone_id", zone_id)
        if allocation_id is not None:
            pulumi.set(__self__, "allocation_id", allocation_id)
        if eni_id is not None:
            pulumi.set(__self__, "eni_id", eni_id)
        if ipv6_address is not None:
            pulumi.set(__self__, "ipv6_address", ipv6_address)
        if private_ipv4_address is not None:
            pulumi.set(__self__, "private_ipv4_address", private_ipv4_address)
        if public_ipv4_address is not None:
            pulumi.set(__self__, "public_ipv4_address", public_ipv4_address)

    @property
    @pulumi.getter(name="vswitchId")
    def vswitch_id(self) -> pulumi.Input[str]:
        """
        The vSwitch in the zone. You can specify only one vSwitch (subnet) in each zone of an NLB instance.
        """
        return pulumi.get(self, "vswitch_id")

    @vswitch_id.setter
    def vswitch_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vswitch_id", value)

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> pulumi.Input[str]:
        """
        The ID of the zone of the NLB instance.
        """
        return pulumi.get(self, "zone_id")

    @zone_id.setter
    def zone_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "zone_id", value)

    @property
    @pulumi.getter(name="allocationId")
    def allocation_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the EIP associated with the Internet-facing NLB instance.
        """
        return pulumi.get(self, "allocation_id")

    @allocation_id.setter
    def allocation_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "allocation_id", value)

    @property
    @pulumi.getter(name="eniId")
    def eni_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the elastic network interface (ENI).
        """
        return pulumi.get(self, "eni_id")

    @eni_id.setter
    def eni_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "eni_id", value)

    @property
    @pulumi.getter(name="ipv6Address")
    def ipv6_address(self) -> Optional[pulumi.Input[str]]:
        """
        The IPv6 address of the NLB instance.
        """
        return pulumi.get(self, "ipv6_address")

    @ipv6_address.setter
    def ipv6_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ipv6_address", value)

    @property
    @pulumi.getter(name="privateIpv4Address")
    def private_ipv4_address(self) -> Optional[pulumi.Input[str]]:
        """
        The private IPv4 address of the NLB instance.
        """
        return pulumi.get(self, "private_ipv4_address")

    @private_ipv4_address.setter
    def private_ipv4_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_ipv4_address", value)

    @property
    @pulumi.getter(name="publicIpv4Address")
    def public_ipv4_address(self) -> Optional[pulumi.Input[str]]:
        """
        The public IPv4 address of the NLB instance.
        """
        return pulumi.get(self, "public_ipv4_address")

    @public_ipv4_address.setter
    def public_ipv4_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_ipv4_address", value)


@pulumi.input_type
class ServerGroupHealthCheckArgs:
    def __init__(__self__, *,
                 health_check_connect_port: Optional[pulumi.Input[int]] = None,
                 health_check_connect_timeout: Optional[pulumi.Input[int]] = None,
                 health_check_domain: Optional[pulumi.Input[str]] = None,
                 health_check_enabled: Optional[pulumi.Input[bool]] = None,
                 health_check_http_codes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 health_check_interval: Optional[pulumi.Input[int]] = None,
                 health_check_type: Optional[pulumi.Input[str]] = None,
                 health_check_url: Optional[pulumi.Input[str]] = None,
                 healthy_threshold: Optional[pulumi.Input[int]] = None,
                 http_check_method: Optional[pulumi.Input[str]] = None,
                 unhealthy_threshold: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[int] health_check_connect_port: The backend port that is used for health checks. Valid values: 0 to 65535. Default value: 0. If you set the value to 0, the port of a backend server is used for health checks.
        :param pulumi.Input[int] health_check_connect_timeout: The maximum timeout period of a health check response. Unit: seconds. Valid values: 1 to 300. Default value: 5.
        :param pulumi.Input[str] health_check_domain: The domain name that is used for health checks. Valid values:
               - `$SERVER_IP`: the private IP address of a backend server.
        :param pulumi.Input[bool] health_check_enabled: Specifies whether to enable health checks.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] health_check_http_codes: The HTTP status codes to return to health checks. Separate multiple HTTP status codes with commas (,). Valid values: http_2xx (default), http_3xx, http_4xx, and http_5xx. **Note:** This parameter takes effect only if `health_check_type` is set to `http`.
        :param pulumi.Input[int] health_check_interval: The interval between two consecutive health checks. Unit: seconds. Valid values: 5 to 5000. Default value: 10.
        :param pulumi.Input[str] health_check_type: The protocol that is used for health checks. Valid values: `TCP` (default) and `HTTP`.
        :param pulumi.Input[str] health_check_url: The path to which health check requests are sent. The path must be 1 to 80 characters in length, and can contain only letters, digits, and the following special characters: `- / . % ? # & =`. It can also contain the following extended characters: `_ ; ~ ! ( ) * [ ] @ $ ^ : ' , +`. The path must start with a forward slash (/). **Note:** This parameter takes effect only if `health_check_type` is set to `http`.
        :param pulumi.Input[int] healthy_threshold: The number of times that an unhealthy backend server must consecutively pass health checks before it is declared healthy. In this case, the health status is changed from fail to success. Valid values: 2 to 10. Default value: 2.
        :param pulumi.Input[str] http_check_method: The HTTP method that is used for health checks. Valid values: `GET` and `HEAD`. **Note:** This parameter takes effect only if `health_check_type` is set to `http`.
        :param pulumi.Input[int] unhealthy_threshold: The number of times that a healthy backend server must consecutively fail health checks before it is declared unhealthy. In this case, the health status is changed from success to fail. Valid values: 2 to 10. Default value: 2.
        """
        if health_check_connect_port is not None:
            pulumi.set(__self__, "health_check_connect_port", health_check_connect_port)
        if health_check_connect_timeout is not None:
            pulumi.set(__self__, "health_check_connect_timeout", health_check_connect_timeout)
        if health_check_domain is not None:
            pulumi.set(__self__, "health_check_domain", health_check_domain)
        if health_check_enabled is not None:
            pulumi.set(__self__, "health_check_enabled", health_check_enabled)
        if health_check_http_codes is not None:
            pulumi.set(__self__, "health_check_http_codes", health_check_http_codes)
        if health_check_interval is not None:
            pulumi.set(__self__, "health_check_interval", health_check_interval)
        if health_check_type is not None:
            pulumi.set(__self__, "health_check_type", health_check_type)
        if health_check_url is not None:
            pulumi.set(__self__, "health_check_url", health_check_url)
        if healthy_threshold is not None:
            pulumi.set(__self__, "healthy_threshold", healthy_threshold)
        if http_check_method is not None:
            pulumi.set(__self__, "http_check_method", http_check_method)
        if unhealthy_threshold is not None:
            pulumi.set(__self__, "unhealthy_threshold", unhealthy_threshold)

    @property
    @pulumi.getter(name="healthCheckConnectPort")
    def health_check_connect_port(self) -> Optional[pulumi.Input[int]]:
        """
        The backend port that is used for health checks. Valid values: 0 to 65535. Default value: 0. If you set the value to 0, the port of a backend server is used for health checks.
        """
        return pulumi.get(self, "health_check_connect_port")

    @health_check_connect_port.setter
    def health_check_connect_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "health_check_connect_port", value)

    @property
    @pulumi.getter(name="healthCheckConnectTimeout")
    def health_check_connect_timeout(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum timeout period of a health check response. Unit: seconds. Valid values: 1 to 300. Default value: 5.
        """
        return pulumi.get(self, "health_check_connect_timeout")

    @health_check_connect_timeout.setter
    def health_check_connect_timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "health_check_connect_timeout", value)

    @property
    @pulumi.getter(name="healthCheckDomain")
    def health_check_domain(self) -> Optional[pulumi.Input[str]]:
        """
        The domain name that is used for health checks. Valid values:
        - `$SERVER_IP`: the private IP address of a backend server.
        """
        return pulumi.get(self, "health_check_domain")

    @health_check_domain.setter
    def health_check_domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "health_check_domain", value)

    @property
    @pulumi.getter(name="healthCheckEnabled")
    def health_check_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to enable health checks.
        """
        return pulumi.get(self, "health_check_enabled")

    @health_check_enabled.setter
    def health_check_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "health_check_enabled", value)

    @property
    @pulumi.getter(name="healthCheckHttpCodes")
    def health_check_http_codes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The HTTP status codes to return to health checks. Separate multiple HTTP status codes with commas (,). Valid values: http_2xx (default), http_3xx, http_4xx, and http_5xx. **Note:** This parameter takes effect only if `health_check_type` is set to `http`.
        """
        return pulumi.get(self, "health_check_http_codes")

    @health_check_http_codes.setter
    def health_check_http_codes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "health_check_http_codes", value)

    @property
    @pulumi.getter(name="healthCheckInterval")
    def health_check_interval(self) -> Optional[pulumi.Input[int]]:
        """
        The interval between two consecutive health checks. Unit: seconds. Valid values: 5 to 5000. Default value: 10.
        """
        return pulumi.get(self, "health_check_interval")

    @health_check_interval.setter
    def health_check_interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "health_check_interval", value)

    @property
    @pulumi.getter(name="healthCheckType")
    def health_check_type(self) -> Optional[pulumi.Input[str]]:
        """
        The protocol that is used for health checks. Valid values: `TCP` (default) and `HTTP`.
        """
        return pulumi.get(self, "health_check_type")

    @health_check_type.setter
    def health_check_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "health_check_type", value)

    @property
    @pulumi.getter(name="healthCheckUrl")
    def health_check_url(self) -> Optional[pulumi.Input[str]]:
        """
        The path to which health check requests are sent. The path must be 1 to 80 characters in length, and can contain only letters, digits, and the following special characters: `- / . % ? # & =`. It can also contain the following extended characters: `_ ; ~ ! ( ) * [ ] @ $ ^ : ' , +`. The path must start with a forward slash (/). **Note:** This parameter takes effect only if `health_check_type` is set to `http`.
        """
        return pulumi.get(self, "health_check_url")

    @health_check_url.setter
    def health_check_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "health_check_url", value)

    @property
    @pulumi.getter(name="healthyThreshold")
    def healthy_threshold(self) -> Optional[pulumi.Input[int]]:
        """
        The number of times that an unhealthy backend server must consecutively pass health checks before it is declared healthy. In this case, the health status is changed from fail to success. Valid values: 2 to 10. Default value: 2.
        """
        return pulumi.get(self, "healthy_threshold")

    @healthy_threshold.setter
    def healthy_threshold(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "healthy_threshold", value)

    @property
    @pulumi.getter(name="httpCheckMethod")
    def http_check_method(self) -> Optional[pulumi.Input[str]]:
        """
        The HTTP method that is used for health checks. Valid values: `GET` and `HEAD`. **Note:** This parameter takes effect only if `health_check_type` is set to `http`.
        """
        return pulumi.get(self, "http_check_method")

    @http_check_method.setter
    def http_check_method(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "http_check_method", value)

    @property
    @pulumi.getter(name="unhealthyThreshold")
    def unhealthy_threshold(self) -> Optional[pulumi.Input[int]]:
        """
        The number of times that a healthy backend server must consecutively fail health checks before it is declared unhealthy. In this case, the health status is changed from success to fail. Valid values: 2 to 10. Default value: 2.
        """
        return pulumi.get(self, "unhealthy_threshold")

    @unhealthy_threshold.setter
    def unhealthy_threshold(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "unhealthy_threshold", value)


