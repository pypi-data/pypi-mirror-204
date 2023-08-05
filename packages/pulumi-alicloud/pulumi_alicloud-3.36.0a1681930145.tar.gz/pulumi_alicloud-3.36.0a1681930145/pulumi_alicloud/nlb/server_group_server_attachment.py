# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ServerGroupServerAttachmentArgs', 'ServerGroupServerAttachment']

@pulumi.input_type
class ServerGroupServerAttachmentArgs:
    def __init__(__self__, *,
                 port: pulumi.Input[int],
                 server_group_id: pulumi.Input[str],
                 server_id: pulumi.Input[str],
                 server_type: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 server_ip: Optional[pulumi.Input[str]] = None,
                 weight: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a ServerGroupServerAttachment resource.
        :param pulumi.Input[int] port: The port used by the backend server. Valid values: 1 to 65535.
        :param pulumi.Input[str] server_group_id: The ID of the server group.
        :param pulumi.Input[str] server_id: The ID of the server.
               - If the server group type is Instance, set the ServerId parameter to the ID of an Elastic Compute Service (ECS) instance, an elastic network interface (ENI), or an elastic container instance. These backend servers are specified by Ecs, Eni, or Eci.
               - If the server group type is Ip, set the ServerId parameter to an IP address.
        :param pulumi.Input[str] server_type: The type of the backend server. Valid values: `Ecs`, `Eni`, `Eci`, `Ip`.
        :param pulumi.Input[str] description: The description of the servers. The description must be 2 to 256 characters in length, and can contain letters, digits, commas (,), periods (.), semicolons (;), forward slashes (/), at signs (@), underscores (_), and hyphens (-).
        :param pulumi.Input[str] server_ip: The IP address of the server. If the server group type is Ip, set the ServerId parameter to an IP address.
        :param pulumi.Input[int] weight: The weight of the backend server. Valid values: 0 to 100. Default value: 100. If the weight of a backend server is set to 0, no requests are forwarded to the backend server.
        """
        pulumi.set(__self__, "port", port)
        pulumi.set(__self__, "server_group_id", server_group_id)
        pulumi.set(__self__, "server_id", server_id)
        pulumi.set(__self__, "server_type", server_type)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if server_ip is not None:
            pulumi.set(__self__, "server_ip", server_ip)
        if weight is not None:
            pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter
    def port(self) -> pulumi.Input[int]:
        """
        The port used by the backend server. Valid values: 1 to 65535.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: pulumi.Input[int]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter(name="serverGroupId")
    def server_group_id(self) -> pulumi.Input[str]:
        """
        The ID of the server group.
        """
        return pulumi.get(self, "server_group_id")

    @server_group_id.setter
    def server_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_group_id", value)

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> pulumi.Input[str]:
        """
        The ID of the server.
        - If the server group type is Instance, set the ServerId parameter to the ID of an Elastic Compute Service (ECS) instance, an elastic network interface (ENI), or an elastic container instance. These backend servers are specified by Ecs, Eni, or Eci.
        - If the server group type is Ip, set the ServerId parameter to an IP address.
        """
        return pulumi.get(self, "server_id")

    @server_id.setter
    def server_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_id", value)

    @property
    @pulumi.getter(name="serverType")
    def server_type(self) -> pulumi.Input[str]:
        """
        The type of the backend server. Valid values: `Ecs`, `Eni`, `Eci`, `Ip`.
        """
        return pulumi.get(self, "server_type")

    @server_type.setter
    def server_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_type", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the servers. The description must be 2 to 256 characters in length, and can contain letters, digits, commas (,), periods (.), semicolons (;), forward slashes (/), at signs (@), underscores (_), and hyphens (-).
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="serverIp")
    def server_ip(self) -> Optional[pulumi.Input[str]]:
        """
        The IP address of the server. If the server group type is Ip, set the ServerId parameter to an IP address.
        """
        return pulumi.get(self, "server_ip")

    @server_ip.setter
    def server_ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_ip", value)

    @property
    @pulumi.getter
    def weight(self) -> Optional[pulumi.Input[int]]:
        """
        The weight of the backend server. Valid values: 0 to 100. Default value: 100. If the weight of a backend server is set to 0, no requests are forwarded to the backend server.
        """
        return pulumi.get(self, "weight")

    @weight.setter
    def weight(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "weight", value)


@pulumi.input_type
class _ServerGroupServerAttachmentState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 server_group_id: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 server_ip: Optional[pulumi.Input[str]] = None,
                 server_type: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 weight: Optional[pulumi.Input[int]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ServerGroupServerAttachment resources.
        :param pulumi.Input[str] description: The description of the servers. The description must be 2 to 256 characters in length, and can contain letters, digits, commas (,), periods (.), semicolons (;), forward slashes (/), at signs (@), underscores (_), and hyphens (-).
        :param pulumi.Input[int] port: The port used by the backend server. Valid values: 1 to 65535.
        :param pulumi.Input[str] server_group_id: The ID of the server group.
        :param pulumi.Input[str] server_id: The ID of the server.
               - If the server group type is Instance, set the ServerId parameter to the ID of an Elastic Compute Service (ECS) instance, an elastic network interface (ENI), or an elastic container instance. These backend servers are specified by Ecs, Eni, or Eci.
               - If the server group type is Ip, set the ServerId parameter to an IP address.
        :param pulumi.Input[str] server_ip: The IP address of the server. If the server group type is Ip, set the ServerId parameter to an IP address.
        :param pulumi.Input[str] server_type: The type of the backend server. Valid values: `Ecs`, `Eni`, `Eci`, `Ip`.
        :param pulumi.Input[str] status: Status of the server.
        :param pulumi.Input[int] weight: The weight of the backend server. Valid values: 0 to 100. Default value: 100. If the weight of a backend server is set to 0, no requests are forwarded to the backend server.
        :param pulumi.Input[str] zone_id: The zoneId of the server.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if server_group_id is not None:
            pulumi.set(__self__, "server_group_id", server_group_id)
        if server_id is not None:
            pulumi.set(__self__, "server_id", server_id)
        if server_ip is not None:
            pulumi.set(__self__, "server_ip", server_ip)
        if server_type is not None:
            pulumi.set(__self__, "server_type", server_type)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if weight is not None:
            pulumi.set(__self__, "weight", weight)
        if zone_id is not None:
            pulumi.set(__self__, "zone_id", zone_id)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the servers. The description must be 2 to 256 characters in length, and can contain letters, digits, commas (,), periods (.), semicolons (;), forward slashes (/), at signs (@), underscores (_), and hyphens (-).
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        The port used by the backend server. Valid values: 1 to 65535.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter(name="serverGroupId")
    def server_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the server group.
        """
        return pulumi.get(self, "server_group_id")

    @server_group_id.setter
    def server_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_group_id", value)

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the server.
        - If the server group type is Instance, set the ServerId parameter to the ID of an Elastic Compute Service (ECS) instance, an elastic network interface (ENI), or an elastic container instance. These backend servers are specified by Ecs, Eni, or Eci.
        - If the server group type is Ip, set the ServerId parameter to an IP address.
        """
        return pulumi.get(self, "server_id")

    @server_id.setter
    def server_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_id", value)

    @property
    @pulumi.getter(name="serverIp")
    def server_ip(self) -> Optional[pulumi.Input[str]]:
        """
        The IP address of the server. If the server group type is Ip, set the ServerId parameter to an IP address.
        """
        return pulumi.get(self, "server_ip")

    @server_ip.setter
    def server_ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_ip", value)

    @property
    @pulumi.getter(name="serverType")
    def server_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the backend server. Valid values: `Ecs`, `Eni`, `Eci`, `Ip`.
        """
        return pulumi.get(self, "server_type")

    @server_type.setter
    def server_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_type", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Status of the server.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def weight(self) -> Optional[pulumi.Input[int]]:
        """
        The weight of the backend server. Valid values: 0 to 100. Default value: 100. If the weight of a backend server is set to 0, no requests are forwarded to the backend server.
        """
        return pulumi.get(self, "weight")

    @weight.setter
    def weight(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "weight", value)

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        The zoneId of the server.
        """
        return pulumi.get(self, "zone_id")

    @zone_id.setter
    def zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone_id", value)


class ServerGroupServerAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 server_group_id: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 server_ip: Optional[pulumi.Input[str]] = None,
                 server_type: Optional[pulumi.Input[str]] = None,
                 weight: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Provides a NLB Server Group Server Attachment resource.

        For information about NLB Server Group Server Attachment and how to use it, see [What is Server Group Server Attachment](https://www.alibabacloud.com/help/en/server-load-balancer/latest/addserverstoservergroup-nlb).

        > **NOTE:** Available in v1.192.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default_networks = alicloud.vpc.get_networks(name_regex="default-NODELETING")
        default_resource_groups = alicloud.resourcemanager.get_resource_groups()
        default_server_group = alicloud.nlb.ServerGroup("defaultServerGroup",
            resource_group_id=default_resource_groups.ids[0],
            server_group_name=var["name"],
            server_group_type="Ip",
            vpc_id=default_networks.ids[0],
            scheduler="Wrr",
            protocol="TCP",
            health_check=alicloud.nlb.ServerGroupHealthCheckArgs(
                health_check_enabled=False,
            ),
            address_ip_version="Ipv4")
        default_server_group_server_attachment = alicloud.nlb.ServerGroupServerAttachment("defaultServerGroupServerAttachment",
            server_type="Ip",
            server_id="10.0.0.0",
            description=var["name"],
            port=80,
            server_group_id=default_server_group.id,
            weight=100,
            server_ip="10.0.0.0")
        ```

        ## Import

        NLB Server Group Server Attachment can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:nlb/serverGroupServerAttachment:ServerGroupServerAttachment example <server_group_id>:<server_id>:<server_type>:<port>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the servers. The description must be 2 to 256 characters in length, and can contain letters, digits, commas (,), periods (.), semicolons (;), forward slashes (/), at signs (@), underscores (_), and hyphens (-).
        :param pulumi.Input[int] port: The port used by the backend server. Valid values: 1 to 65535.
        :param pulumi.Input[str] server_group_id: The ID of the server group.
        :param pulumi.Input[str] server_id: The ID of the server.
               - If the server group type is Instance, set the ServerId parameter to the ID of an Elastic Compute Service (ECS) instance, an elastic network interface (ENI), or an elastic container instance. These backend servers are specified by Ecs, Eni, or Eci.
               - If the server group type is Ip, set the ServerId parameter to an IP address.
        :param pulumi.Input[str] server_ip: The IP address of the server. If the server group type is Ip, set the ServerId parameter to an IP address.
        :param pulumi.Input[str] server_type: The type of the backend server. Valid values: `Ecs`, `Eni`, `Eci`, `Ip`.
        :param pulumi.Input[int] weight: The weight of the backend server. Valid values: 0 to 100. Default value: 100. If the weight of a backend server is set to 0, no requests are forwarded to the backend server.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServerGroupServerAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a NLB Server Group Server Attachment resource.

        For information about NLB Server Group Server Attachment and how to use it, see [What is Server Group Server Attachment](https://www.alibabacloud.com/help/en/server-load-balancer/latest/addserverstoservergroup-nlb).

        > **NOTE:** Available in v1.192.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default_networks = alicloud.vpc.get_networks(name_regex="default-NODELETING")
        default_resource_groups = alicloud.resourcemanager.get_resource_groups()
        default_server_group = alicloud.nlb.ServerGroup("defaultServerGroup",
            resource_group_id=default_resource_groups.ids[0],
            server_group_name=var["name"],
            server_group_type="Ip",
            vpc_id=default_networks.ids[0],
            scheduler="Wrr",
            protocol="TCP",
            health_check=alicloud.nlb.ServerGroupHealthCheckArgs(
                health_check_enabled=False,
            ),
            address_ip_version="Ipv4")
        default_server_group_server_attachment = alicloud.nlb.ServerGroupServerAttachment("defaultServerGroupServerAttachment",
            server_type="Ip",
            server_id="10.0.0.0",
            description=var["name"],
            port=80,
            server_group_id=default_server_group.id,
            weight=100,
            server_ip="10.0.0.0")
        ```

        ## Import

        NLB Server Group Server Attachment can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:nlb/serverGroupServerAttachment:ServerGroupServerAttachment example <server_group_id>:<server_id>:<server_type>:<port>
        ```

        :param str resource_name: The name of the resource.
        :param ServerGroupServerAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServerGroupServerAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 server_group_id: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 server_ip: Optional[pulumi.Input[str]] = None,
                 server_type: Optional[pulumi.Input[str]] = None,
                 weight: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServerGroupServerAttachmentArgs.__new__(ServerGroupServerAttachmentArgs)

            __props__.__dict__["description"] = description
            if port is None and not opts.urn:
                raise TypeError("Missing required property 'port'")
            __props__.__dict__["port"] = port
            if server_group_id is None and not opts.urn:
                raise TypeError("Missing required property 'server_group_id'")
            __props__.__dict__["server_group_id"] = server_group_id
            if server_id is None and not opts.urn:
                raise TypeError("Missing required property 'server_id'")
            __props__.__dict__["server_id"] = server_id
            __props__.__dict__["server_ip"] = server_ip
            if server_type is None and not opts.urn:
                raise TypeError("Missing required property 'server_type'")
            __props__.__dict__["server_type"] = server_type
            __props__.__dict__["weight"] = weight
            __props__.__dict__["status"] = None
            __props__.__dict__["zone_id"] = None
        super(ServerGroupServerAttachment, __self__).__init__(
            'alicloud:nlb/serverGroupServerAttachment:ServerGroupServerAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            port: Optional[pulumi.Input[int]] = None,
            server_group_id: Optional[pulumi.Input[str]] = None,
            server_id: Optional[pulumi.Input[str]] = None,
            server_ip: Optional[pulumi.Input[str]] = None,
            server_type: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            weight: Optional[pulumi.Input[int]] = None,
            zone_id: Optional[pulumi.Input[str]] = None) -> 'ServerGroupServerAttachment':
        """
        Get an existing ServerGroupServerAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the servers. The description must be 2 to 256 characters in length, and can contain letters, digits, commas (,), periods (.), semicolons (;), forward slashes (/), at signs (@), underscores (_), and hyphens (-).
        :param pulumi.Input[int] port: The port used by the backend server. Valid values: 1 to 65535.
        :param pulumi.Input[str] server_group_id: The ID of the server group.
        :param pulumi.Input[str] server_id: The ID of the server.
               - If the server group type is Instance, set the ServerId parameter to the ID of an Elastic Compute Service (ECS) instance, an elastic network interface (ENI), or an elastic container instance. These backend servers are specified by Ecs, Eni, or Eci.
               - If the server group type is Ip, set the ServerId parameter to an IP address.
        :param pulumi.Input[str] server_ip: The IP address of the server. If the server group type is Ip, set the ServerId parameter to an IP address.
        :param pulumi.Input[str] server_type: The type of the backend server. Valid values: `Ecs`, `Eni`, `Eci`, `Ip`.
        :param pulumi.Input[str] status: Status of the server.
        :param pulumi.Input[int] weight: The weight of the backend server. Valid values: 0 to 100. Default value: 100. If the weight of a backend server is set to 0, no requests are forwarded to the backend server.
        :param pulumi.Input[str] zone_id: The zoneId of the server.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServerGroupServerAttachmentState.__new__(_ServerGroupServerAttachmentState)

        __props__.__dict__["description"] = description
        __props__.__dict__["port"] = port
        __props__.__dict__["server_group_id"] = server_group_id
        __props__.__dict__["server_id"] = server_id
        __props__.__dict__["server_ip"] = server_ip
        __props__.__dict__["server_type"] = server_type
        __props__.__dict__["status"] = status
        __props__.__dict__["weight"] = weight
        __props__.__dict__["zone_id"] = zone_id
        return ServerGroupServerAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the servers. The description must be 2 to 256 characters in length, and can contain letters, digits, commas (,), periods (.), semicolons (;), forward slashes (/), at signs (@), underscores (_), and hyphens (-).
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[int]:
        """
        The port used by the backend server. Valid values: 1 to 65535.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="serverGroupId")
    def server_group_id(self) -> pulumi.Output[str]:
        """
        The ID of the server group.
        """
        return pulumi.get(self, "server_group_id")

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> pulumi.Output[str]:
        """
        The ID of the server.
        - If the server group type is Instance, set the ServerId parameter to the ID of an Elastic Compute Service (ECS) instance, an elastic network interface (ENI), or an elastic container instance. These backend servers are specified by Ecs, Eni, or Eci.
        - If the server group type is Ip, set the ServerId parameter to an IP address.
        """
        return pulumi.get(self, "server_id")

    @property
    @pulumi.getter(name="serverIp")
    def server_ip(self) -> pulumi.Output[str]:
        """
        The IP address of the server. If the server group type is Ip, set the ServerId parameter to an IP address.
        """
        return pulumi.get(self, "server_ip")

    @property
    @pulumi.getter(name="serverType")
    def server_type(self) -> pulumi.Output[str]:
        """
        The type of the backend server. Valid values: `Ecs`, `Eni`, `Eci`, `Ip`.
        """
        return pulumi.get(self, "server_type")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Status of the server.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def weight(self) -> pulumi.Output[int]:
        """
        The weight of the backend server. Valid values: 0 to 100. Default value: 100. If the weight of a backend server is set to 0, no requests are forwarded to the backend server.
        """
        return pulumi.get(self, "weight")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> pulumi.Output[str]:
        """
        The zoneId of the server.
        """
        return pulumi.get(self, "zone_id")

