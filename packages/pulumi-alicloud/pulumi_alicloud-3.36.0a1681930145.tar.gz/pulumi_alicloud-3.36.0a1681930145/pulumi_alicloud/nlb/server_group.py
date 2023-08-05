# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['ServerGroupArgs', 'ServerGroup']

@pulumi.input_type
class ServerGroupArgs:
    def __init__(__self__, *,
                 health_check: pulumi.Input['ServerGroupHealthCheckArgs'],
                 server_group_name: pulumi.Input[str],
                 vpc_id: pulumi.Input[str],
                 address_ip_version: Optional[pulumi.Input[str]] = None,
                 connection_drain: Optional[pulumi.Input[bool]] = None,
                 connection_drain_timeout: Optional[pulumi.Input[int]] = None,
                 preserve_client_ip_enabled: Optional[pulumi.Input[bool]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 scheduler: Optional[pulumi.Input[str]] = None,
                 server_group_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None):
        """
        The set of arguments for constructing a ServerGroup resource.
        :param pulumi.Input['ServerGroupHealthCheckArgs'] health_check: HealthCheck. See the following `Block health_check`.
        :param pulumi.Input[str] server_group_name: The name of the server group. The name must be 2 to 128 characters in length, and can contain letters, digits, periods (.), underscores (_), and hyphens (-). The name must start with a letter.
        :param pulumi.Input[str] vpc_id: The id of the vpc.
        :param pulumi.Input[str] address_ip_version: The protocol version. Valid values: `Ipv4` (default), `DualStack`.
        :param pulumi.Input[bool] connection_drain: Specifies whether to enable connection draining.
        :param pulumi.Input[int] connection_drain_timeout: The timeout period of connection draining. Unit: seconds. Valid values: 10 to 900.
        :param pulumi.Input[bool] preserve_client_ip_enabled: Indicates whether client address retention is enabled.
        :param pulumi.Input[str] protocol: The backend protocol. Valid values: `TCP` (default), `UDP`, and `TCPSSL`.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group to which the security group belongs.
        :param pulumi.Input[str] scheduler: The routing algorithm. Valid values:
        :param pulumi.Input[str] server_group_type: The type of the server group. Valid values:
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        """
        pulumi.set(__self__, "health_check", health_check)
        pulumi.set(__self__, "server_group_name", server_group_name)
        pulumi.set(__self__, "vpc_id", vpc_id)
        if address_ip_version is not None:
            pulumi.set(__self__, "address_ip_version", address_ip_version)
        if connection_drain is not None:
            pulumi.set(__self__, "connection_drain", connection_drain)
        if connection_drain_timeout is not None:
            pulumi.set(__self__, "connection_drain_timeout", connection_drain_timeout)
        if preserve_client_ip_enabled is not None:
            pulumi.set(__self__, "preserve_client_ip_enabled", preserve_client_ip_enabled)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)
        if resource_group_id is not None:
            pulumi.set(__self__, "resource_group_id", resource_group_id)
        if scheduler is not None:
            pulumi.set(__self__, "scheduler", scheduler)
        if server_group_type is not None:
            pulumi.set(__self__, "server_group_type", server_group_type)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="healthCheck")
    def health_check(self) -> pulumi.Input['ServerGroupHealthCheckArgs']:
        """
        HealthCheck. See the following `Block health_check`.
        """
        return pulumi.get(self, "health_check")

    @health_check.setter
    def health_check(self, value: pulumi.Input['ServerGroupHealthCheckArgs']):
        pulumi.set(self, "health_check", value)

    @property
    @pulumi.getter(name="serverGroupName")
    def server_group_name(self) -> pulumi.Input[str]:
        """
        The name of the server group. The name must be 2 to 128 characters in length, and can contain letters, digits, periods (.), underscores (_), and hyphens (-). The name must start with a letter.
        """
        return pulumi.get(self, "server_group_name")

    @server_group_name.setter
    def server_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_group_name", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Input[str]:
        """
        The id of the vpc.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc_id", value)

    @property
    @pulumi.getter(name="addressIpVersion")
    def address_ip_version(self) -> Optional[pulumi.Input[str]]:
        """
        The protocol version. Valid values: `Ipv4` (default), `DualStack`.
        """
        return pulumi.get(self, "address_ip_version")

    @address_ip_version.setter
    def address_ip_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address_ip_version", value)

    @property
    @pulumi.getter(name="connectionDrain")
    def connection_drain(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to enable connection draining.
        """
        return pulumi.get(self, "connection_drain")

    @connection_drain.setter
    def connection_drain(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "connection_drain", value)

    @property
    @pulumi.getter(name="connectionDrainTimeout")
    def connection_drain_timeout(self) -> Optional[pulumi.Input[int]]:
        """
        The timeout period of connection draining. Unit: seconds. Valid values: 10 to 900.
        """
        return pulumi.get(self, "connection_drain_timeout")

    @connection_drain_timeout.setter
    def connection_drain_timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "connection_drain_timeout", value)

    @property
    @pulumi.getter(name="preserveClientIpEnabled")
    def preserve_client_ip_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether client address retention is enabled.
        """
        return pulumi.get(self, "preserve_client_ip_enabled")

    @preserve_client_ip_enabled.setter
    def preserve_client_ip_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "preserve_client_ip_enabled", value)

    @property
    @pulumi.getter
    def protocol(self) -> Optional[pulumi.Input[str]]:
        """
        The backend protocol. Valid values: `TCP` (default), `UDP`, and `TCPSSL`.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the resource group to which the security group belongs.
        """
        return pulumi.get(self, "resource_group_id")

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_id", value)

    @property
    @pulumi.getter
    def scheduler(self) -> Optional[pulumi.Input[str]]:
        """
        The routing algorithm. Valid values:
        """
        return pulumi.get(self, "scheduler")

    @scheduler.setter
    def scheduler(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scheduler", value)

    @property
    @pulumi.getter(name="serverGroupType")
    def server_group_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the server group. Valid values:
        """
        return pulumi.get(self, "server_group_type")

    @server_group_type.setter
    def server_group_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_group_type", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ServerGroupState:
    def __init__(__self__, *,
                 address_ip_version: Optional[pulumi.Input[str]] = None,
                 connection_drain: Optional[pulumi.Input[bool]] = None,
                 connection_drain_timeout: Optional[pulumi.Input[int]] = None,
                 health_check: Optional[pulumi.Input['ServerGroupHealthCheckArgs']] = None,
                 preserve_client_ip_enabled: Optional[pulumi.Input[bool]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 scheduler: Optional[pulumi.Input[str]] = None,
                 server_group_name: Optional[pulumi.Input[str]] = None,
                 server_group_type: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ServerGroup resources.
        :param pulumi.Input[str] address_ip_version: The protocol version. Valid values: `Ipv4` (default), `DualStack`.
        :param pulumi.Input[bool] connection_drain: Specifies whether to enable connection draining.
        :param pulumi.Input[int] connection_drain_timeout: The timeout period of connection draining. Unit: seconds. Valid values: 10 to 900.
        :param pulumi.Input['ServerGroupHealthCheckArgs'] health_check: HealthCheck. See the following `Block health_check`.
        :param pulumi.Input[bool] preserve_client_ip_enabled: Indicates whether client address retention is enabled.
        :param pulumi.Input[str] protocol: The backend protocol. Valid values: `TCP` (default), `UDP`, and `TCPSSL`.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group to which the security group belongs.
        :param pulumi.Input[str] scheduler: The routing algorithm. Valid values:
        :param pulumi.Input[str] server_group_name: The name of the server group. The name must be 2 to 128 characters in length, and can contain letters, digits, periods (.), underscores (_), and hyphens (-). The name must start with a letter.
        :param pulumi.Input[str] server_group_type: The type of the server group. Valid values:
        :param pulumi.Input[str] status: The status of the resource.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] vpc_id: The id of the vpc.
        """
        if address_ip_version is not None:
            pulumi.set(__self__, "address_ip_version", address_ip_version)
        if connection_drain is not None:
            pulumi.set(__self__, "connection_drain", connection_drain)
        if connection_drain_timeout is not None:
            pulumi.set(__self__, "connection_drain_timeout", connection_drain_timeout)
        if health_check is not None:
            pulumi.set(__self__, "health_check", health_check)
        if preserve_client_ip_enabled is not None:
            pulumi.set(__self__, "preserve_client_ip_enabled", preserve_client_ip_enabled)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)
        if resource_group_id is not None:
            pulumi.set(__self__, "resource_group_id", resource_group_id)
        if scheduler is not None:
            pulumi.set(__self__, "scheduler", scheduler)
        if server_group_name is not None:
            pulumi.set(__self__, "server_group_name", server_group_name)
        if server_group_type is not None:
            pulumi.set(__self__, "server_group_type", server_group_type)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="addressIpVersion")
    def address_ip_version(self) -> Optional[pulumi.Input[str]]:
        """
        The protocol version. Valid values: `Ipv4` (default), `DualStack`.
        """
        return pulumi.get(self, "address_ip_version")

    @address_ip_version.setter
    def address_ip_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address_ip_version", value)

    @property
    @pulumi.getter(name="connectionDrain")
    def connection_drain(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to enable connection draining.
        """
        return pulumi.get(self, "connection_drain")

    @connection_drain.setter
    def connection_drain(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "connection_drain", value)

    @property
    @pulumi.getter(name="connectionDrainTimeout")
    def connection_drain_timeout(self) -> Optional[pulumi.Input[int]]:
        """
        The timeout period of connection draining. Unit: seconds. Valid values: 10 to 900.
        """
        return pulumi.get(self, "connection_drain_timeout")

    @connection_drain_timeout.setter
    def connection_drain_timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "connection_drain_timeout", value)

    @property
    @pulumi.getter(name="healthCheck")
    def health_check(self) -> Optional[pulumi.Input['ServerGroupHealthCheckArgs']]:
        """
        HealthCheck. See the following `Block health_check`.
        """
        return pulumi.get(self, "health_check")

    @health_check.setter
    def health_check(self, value: Optional[pulumi.Input['ServerGroupHealthCheckArgs']]):
        pulumi.set(self, "health_check", value)

    @property
    @pulumi.getter(name="preserveClientIpEnabled")
    def preserve_client_ip_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether client address retention is enabled.
        """
        return pulumi.get(self, "preserve_client_ip_enabled")

    @preserve_client_ip_enabled.setter
    def preserve_client_ip_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "preserve_client_ip_enabled", value)

    @property
    @pulumi.getter
    def protocol(self) -> Optional[pulumi.Input[str]]:
        """
        The backend protocol. Valid values: `TCP` (default), `UDP`, and `TCPSSL`.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the resource group to which the security group belongs.
        """
        return pulumi.get(self, "resource_group_id")

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_id", value)

    @property
    @pulumi.getter
    def scheduler(self) -> Optional[pulumi.Input[str]]:
        """
        The routing algorithm. Valid values:
        """
        return pulumi.get(self, "scheduler")

    @scheduler.setter
    def scheduler(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scheduler", value)

    @property
    @pulumi.getter(name="serverGroupName")
    def server_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the server group. The name must be 2 to 128 characters in length, and can contain letters, digits, periods (.), underscores (_), and hyphens (-). The name must start with a letter.
        """
        return pulumi.get(self, "server_group_name")

    @server_group_name.setter
    def server_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_group_name", value)

    @property
    @pulumi.getter(name="serverGroupType")
    def server_group_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the server group. Valid values:
        """
        return pulumi.get(self, "server_group_type")

    @server_group_type.setter
    def server_group_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_group_type", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the resource.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the vpc.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_id", value)


class ServerGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address_ip_version: Optional[pulumi.Input[str]] = None,
                 connection_drain: Optional[pulumi.Input[bool]] = None,
                 connection_drain_timeout: Optional[pulumi.Input[int]] = None,
                 health_check: Optional[pulumi.Input[pulumi.InputType['ServerGroupHealthCheckArgs']]] = None,
                 preserve_client_ip_enabled: Optional[pulumi.Input[bool]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 scheduler: Optional[pulumi.Input[str]] = None,
                 server_group_name: Optional[pulumi.Input[str]] = None,
                 server_group_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a NLB Server Group resource.

        For information about NLB Server Group and how to use it, see [What is Server Group](https://www.alibabacloud.com/help/en/server-load-balancer/latest/createservergroup-nlb).

        > **NOTE:** Available in v1.186.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default_resource_groups = alicloud.resourcemanager.get_resource_groups()
        default_networks = alicloud.vpc.get_networks(name_regex="default-NODELETING")
        default_server_group = alicloud.nlb.ServerGroup("defaultServerGroup",
            resource_group_id=default_resource_groups.ids[0],
            server_group_name=var["name"],
            server_group_type="Instance",
            vpc_id=default_networks.ids[0],
            scheduler="Wrr",
            protocol="TCP",
            health_check=alicloud.nlb.ServerGroupHealthCheckArgs(
                health_check_enabled=True,
                health_check_type="TCP",
                health_check_connect_port=0,
                healthy_threshold=2,
                unhealthy_threshold=2,
                health_check_connect_timeout=5,
                health_check_interval=10,
                http_check_method="GET",
                health_check_http_codes=[
                    "http_2xx",
                    "http_3xx",
                    "http_4xx",
                ],
            ),
            connection_drain=True,
            connection_drain_timeout=60,
            tags={
                "Created": "TF",
            },
            address_ip_version="Ipv4")
        ```

        ## Import

        NLB Server Group can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:nlb/serverGroup:ServerGroup example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address_ip_version: The protocol version. Valid values: `Ipv4` (default), `DualStack`.
        :param pulumi.Input[bool] connection_drain: Specifies whether to enable connection draining.
        :param pulumi.Input[int] connection_drain_timeout: The timeout period of connection draining. Unit: seconds. Valid values: 10 to 900.
        :param pulumi.Input[pulumi.InputType['ServerGroupHealthCheckArgs']] health_check: HealthCheck. See the following `Block health_check`.
        :param pulumi.Input[bool] preserve_client_ip_enabled: Indicates whether client address retention is enabled.
        :param pulumi.Input[str] protocol: The backend protocol. Valid values: `TCP` (default), `UDP`, and `TCPSSL`.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group to which the security group belongs.
        :param pulumi.Input[str] scheduler: The routing algorithm. Valid values:
        :param pulumi.Input[str] server_group_name: The name of the server group. The name must be 2 to 128 characters in length, and can contain letters, digits, periods (.), underscores (_), and hyphens (-). The name must start with a letter.
        :param pulumi.Input[str] server_group_type: The type of the server group. Valid values:
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] vpc_id: The id of the vpc.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServerGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a NLB Server Group resource.

        For information about NLB Server Group and how to use it, see [What is Server Group](https://www.alibabacloud.com/help/en/server-load-balancer/latest/createservergroup-nlb).

        > **NOTE:** Available in v1.186.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default_resource_groups = alicloud.resourcemanager.get_resource_groups()
        default_networks = alicloud.vpc.get_networks(name_regex="default-NODELETING")
        default_server_group = alicloud.nlb.ServerGroup("defaultServerGroup",
            resource_group_id=default_resource_groups.ids[0],
            server_group_name=var["name"],
            server_group_type="Instance",
            vpc_id=default_networks.ids[0],
            scheduler="Wrr",
            protocol="TCP",
            health_check=alicloud.nlb.ServerGroupHealthCheckArgs(
                health_check_enabled=True,
                health_check_type="TCP",
                health_check_connect_port=0,
                healthy_threshold=2,
                unhealthy_threshold=2,
                health_check_connect_timeout=5,
                health_check_interval=10,
                http_check_method="GET",
                health_check_http_codes=[
                    "http_2xx",
                    "http_3xx",
                    "http_4xx",
                ],
            ),
            connection_drain=True,
            connection_drain_timeout=60,
            tags={
                "Created": "TF",
            },
            address_ip_version="Ipv4")
        ```

        ## Import

        NLB Server Group can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:nlb/serverGroup:ServerGroup example <id>
        ```

        :param str resource_name: The name of the resource.
        :param ServerGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServerGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address_ip_version: Optional[pulumi.Input[str]] = None,
                 connection_drain: Optional[pulumi.Input[bool]] = None,
                 connection_drain_timeout: Optional[pulumi.Input[int]] = None,
                 health_check: Optional[pulumi.Input[pulumi.InputType['ServerGroupHealthCheckArgs']]] = None,
                 preserve_client_ip_enabled: Optional[pulumi.Input[bool]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 scheduler: Optional[pulumi.Input[str]] = None,
                 server_group_name: Optional[pulumi.Input[str]] = None,
                 server_group_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServerGroupArgs.__new__(ServerGroupArgs)

            __props__.__dict__["address_ip_version"] = address_ip_version
            __props__.__dict__["connection_drain"] = connection_drain
            __props__.__dict__["connection_drain_timeout"] = connection_drain_timeout
            if health_check is None and not opts.urn:
                raise TypeError("Missing required property 'health_check'")
            __props__.__dict__["health_check"] = health_check
            __props__.__dict__["preserve_client_ip_enabled"] = preserve_client_ip_enabled
            __props__.__dict__["protocol"] = protocol
            __props__.__dict__["resource_group_id"] = resource_group_id
            __props__.__dict__["scheduler"] = scheduler
            if server_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_group_name'")
            __props__.__dict__["server_group_name"] = server_group_name
            __props__.__dict__["server_group_type"] = server_group_type
            __props__.__dict__["tags"] = tags
            if vpc_id is None and not opts.urn:
                raise TypeError("Missing required property 'vpc_id'")
            __props__.__dict__["vpc_id"] = vpc_id
            __props__.__dict__["status"] = None
        super(ServerGroup, __self__).__init__(
            'alicloud:nlb/serverGroup:ServerGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            address_ip_version: Optional[pulumi.Input[str]] = None,
            connection_drain: Optional[pulumi.Input[bool]] = None,
            connection_drain_timeout: Optional[pulumi.Input[int]] = None,
            health_check: Optional[pulumi.Input[pulumi.InputType['ServerGroupHealthCheckArgs']]] = None,
            preserve_client_ip_enabled: Optional[pulumi.Input[bool]] = None,
            protocol: Optional[pulumi.Input[str]] = None,
            resource_group_id: Optional[pulumi.Input[str]] = None,
            scheduler: Optional[pulumi.Input[str]] = None,
            server_group_name: Optional[pulumi.Input[str]] = None,
            server_group_type: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            vpc_id: Optional[pulumi.Input[str]] = None) -> 'ServerGroup':
        """
        Get an existing ServerGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address_ip_version: The protocol version. Valid values: `Ipv4` (default), `DualStack`.
        :param pulumi.Input[bool] connection_drain: Specifies whether to enable connection draining.
        :param pulumi.Input[int] connection_drain_timeout: The timeout period of connection draining. Unit: seconds. Valid values: 10 to 900.
        :param pulumi.Input[pulumi.InputType['ServerGroupHealthCheckArgs']] health_check: HealthCheck. See the following `Block health_check`.
        :param pulumi.Input[bool] preserve_client_ip_enabled: Indicates whether client address retention is enabled.
        :param pulumi.Input[str] protocol: The backend protocol. Valid values: `TCP` (default), `UDP`, and `TCPSSL`.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group to which the security group belongs.
        :param pulumi.Input[str] scheduler: The routing algorithm. Valid values:
        :param pulumi.Input[str] server_group_name: The name of the server group. The name must be 2 to 128 characters in length, and can contain letters, digits, periods (.), underscores (_), and hyphens (-). The name must start with a letter.
        :param pulumi.Input[str] server_group_type: The type of the server group. Valid values:
        :param pulumi.Input[str] status: The status of the resource.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] vpc_id: The id of the vpc.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServerGroupState.__new__(_ServerGroupState)

        __props__.__dict__["address_ip_version"] = address_ip_version
        __props__.__dict__["connection_drain"] = connection_drain
        __props__.__dict__["connection_drain_timeout"] = connection_drain_timeout
        __props__.__dict__["health_check"] = health_check
        __props__.__dict__["preserve_client_ip_enabled"] = preserve_client_ip_enabled
        __props__.__dict__["protocol"] = protocol
        __props__.__dict__["resource_group_id"] = resource_group_id
        __props__.__dict__["scheduler"] = scheduler
        __props__.__dict__["server_group_name"] = server_group_name
        __props__.__dict__["server_group_type"] = server_group_type
        __props__.__dict__["status"] = status
        __props__.__dict__["tags"] = tags
        __props__.__dict__["vpc_id"] = vpc_id
        return ServerGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="addressIpVersion")
    def address_ip_version(self) -> pulumi.Output[str]:
        """
        The protocol version. Valid values: `Ipv4` (default), `DualStack`.
        """
        return pulumi.get(self, "address_ip_version")

    @property
    @pulumi.getter(name="connectionDrain")
    def connection_drain(self) -> pulumi.Output[bool]:
        """
        Specifies whether to enable connection draining.
        """
        return pulumi.get(self, "connection_drain")

    @property
    @pulumi.getter(name="connectionDrainTimeout")
    def connection_drain_timeout(self) -> pulumi.Output[int]:
        """
        The timeout period of connection draining. Unit: seconds. Valid values: 10 to 900.
        """
        return pulumi.get(self, "connection_drain_timeout")

    @property
    @pulumi.getter(name="healthCheck")
    def health_check(self) -> pulumi.Output['outputs.ServerGroupHealthCheck']:
        """
        HealthCheck. See the following `Block health_check`.
        """
        return pulumi.get(self, "health_check")

    @property
    @pulumi.getter(name="preserveClientIpEnabled")
    def preserve_client_ip_enabled(self) -> pulumi.Output[bool]:
        """
        Indicates whether client address retention is enabled.
        """
        return pulumi.get(self, "preserve_client_ip_enabled")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output[str]:
        """
        The backend protocol. Valid values: `TCP` (default), `UDP`, and `TCPSSL`.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> pulumi.Output[str]:
        """
        The ID of the resource group to which the security group belongs.
        """
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter
    def scheduler(self) -> pulumi.Output[str]:
        """
        The routing algorithm. Valid values:
        """
        return pulumi.get(self, "scheduler")

    @property
    @pulumi.getter(name="serverGroupName")
    def server_group_name(self) -> pulumi.Output[str]:
        """
        The name of the server group. The name must be 2 to 128 characters in length, and can contain letters, digits, periods (.), underscores (_), and hyphens (-). The name must start with a letter.
        """
        return pulumi.get(self, "server_group_name")

    @property
    @pulumi.getter(name="serverGroupType")
    def server_group_type(self) -> pulumi.Output[str]:
        """
        The type of the server group. Valid values:
        """
        return pulumi.get(self, "server_group_type")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the resource.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[str]:
        """
        The id of the vpc.
        """
        return pulumi.get(self, "vpc_id")

