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

__all__ = ['CustomRoutingEndpointTrafficPolicyArgs', 'CustomRoutingEndpointTrafficPolicy']

@pulumi.input_type
class CustomRoutingEndpointTrafficPolicyArgs:
    def __init__(__self__, *,
                 address: pulumi.Input[str],
                 endpoint_id: pulumi.Input[str],
                 port_ranges: Optional[pulumi.Input[Sequence[pulumi.Input['CustomRoutingEndpointTrafficPolicyPortRangeArgs']]]] = None):
        """
        The set of arguments for constructing a CustomRoutingEndpointTrafficPolicy resource.
        :param pulumi.Input[str] address: The IP address of the destination to which traffic is allowed.
        :param pulumi.Input[str] endpoint_id: The ID of the Custom Routing Endpoint.
        :param pulumi.Input[Sequence[pulumi.Input['CustomRoutingEndpointTrafficPolicyPortRangeArgs']]] port_ranges: Port rangeSee the following. See the following `Block port_ranges`.
        """
        pulumi.set(__self__, "address", address)
        pulumi.set(__self__, "endpoint_id", endpoint_id)
        if port_ranges is not None:
            pulumi.set(__self__, "port_ranges", port_ranges)

    @property
    @pulumi.getter
    def address(self) -> pulumi.Input[str]:
        """
        The IP address of the destination to which traffic is allowed.
        """
        return pulumi.get(self, "address")

    @address.setter
    def address(self, value: pulumi.Input[str]):
        pulumi.set(self, "address", value)

    @property
    @pulumi.getter(name="endpointId")
    def endpoint_id(self) -> pulumi.Input[str]:
        """
        The ID of the Custom Routing Endpoint.
        """
        return pulumi.get(self, "endpoint_id")

    @endpoint_id.setter
    def endpoint_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "endpoint_id", value)

    @property
    @pulumi.getter(name="portRanges")
    def port_ranges(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CustomRoutingEndpointTrafficPolicyPortRangeArgs']]]]:
        """
        Port rangeSee the following. See the following `Block port_ranges`.
        """
        return pulumi.get(self, "port_ranges")

    @port_ranges.setter
    def port_ranges(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CustomRoutingEndpointTrafficPolicyPortRangeArgs']]]]):
        pulumi.set(self, "port_ranges", value)


@pulumi.input_type
class _CustomRoutingEndpointTrafficPolicyState:
    def __init__(__self__, *,
                 accelerator_id: Optional[pulumi.Input[str]] = None,
                 address: Optional[pulumi.Input[str]] = None,
                 custom_routing_endpoint_traffic_policy_id: Optional[pulumi.Input[str]] = None,
                 endpoint_group_id: Optional[pulumi.Input[str]] = None,
                 endpoint_id: Optional[pulumi.Input[str]] = None,
                 listener_id: Optional[pulumi.Input[str]] = None,
                 port_ranges: Optional[pulumi.Input[Sequence[pulumi.Input['CustomRoutingEndpointTrafficPolicyPortRangeArgs']]]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering CustomRoutingEndpointTrafficPolicy resources.
        :param pulumi.Input[str] accelerator_id: The ID of the GA instance.
        :param pulumi.Input[str] address: The IP address of the destination to which traffic is allowed.
        :param pulumi.Input[str] custom_routing_endpoint_traffic_policy_id: The ID of the Custom Routing Endpoint Traffic Policy.
        :param pulumi.Input[str] endpoint_group_id: The ID of the endpoint group.
        :param pulumi.Input[str] endpoint_id: The ID of the Custom Routing Endpoint.
        :param pulumi.Input[str] listener_id: The ID of the listener.
        :param pulumi.Input[Sequence[pulumi.Input['CustomRoutingEndpointTrafficPolicyPortRangeArgs']]] port_ranges: Port rangeSee the following. See the following `Block port_ranges`.
        :param pulumi.Input[str] status: The status of the Custom Routing Endpoint Traffic Policy.
        """
        if accelerator_id is not None:
            pulumi.set(__self__, "accelerator_id", accelerator_id)
        if address is not None:
            pulumi.set(__self__, "address", address)
        if custom_routing_endpoint_traffic_policy_id is not None:
            pulumi.set(__self__, "custom_routing_endpoint_traffic_policy_id", custom_routing_endpoint_traffic_policy_id)
        if endpoint_group_id is not None:
            pulumi.set(__self__, "endpoint_group_id", endpoint_group_id)
        if endpoint_id is not None:
            pulumi.set(__self__, "endpoint_id", endpoint_id)
        if listener_id is not None:
            pulumi.set(__self__, "listener_id", listener_id)
        if port_ranges is not None:
            pulumi.set(__self__, "port_ranges", port_ranges)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="acceleratorId")
    def accelerator_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the GA instance.
        """
        return pulumi.get(self, "accelerator_id")

    @accelerator_id.setter
    def accelerator_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "accelerator_id", value)

    @property
    @pulumi.getter
    def address(self) -> Optional[pulumi.Input[str]]:
        """
        The IP address of the destination to which traffic is allowed.
        """
        return pulumi.get(self, "address")

    @address.setter
    def address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address", value)

    @property
    @pulumi.getter(name="customRoutingEndpointTrafficPolicyId")
    def custom_routing_endpoint_traffic_policy_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Custom Routing Endpoint Traffic Policy.
        """
        return pulumi.get(self, "custom_routing_endpoint_traffic_policy_id")

    @custom_routing_endpoint_traffic_policy_id.setter
    def custom_routing_endpoint_traffic_policy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_routing_endpoint_traffic_policy_id", value)

    @property
    @pulumi.getter(name="endpointGroupId")
    def endpoint_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the endpoint group.
        """
        return pulumi.get(self, "endpoint_group_id")

    @endpoint_group_id.setter
    def endpoint_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_group_id", value)

    @property
    @pulumi.getter(name="endpointId")
    def endpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Custom Routing Endpoint.
        """
        return pulumi.get(self, "endpoint_id")

    @endpoint_id.setter
    def endpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_id", value)

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the listener.
        """
        return pulumi.get(self, "listener_id")

    @listener_id.setter
    def listener_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "listener_id", value)

    @property
    @pulumi.getter(name="portRanges")
    def port_ranges(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CustomRoutingEndpointTrafficPolicyPortRangeArgs']]]]:
        """
        Port rangeSee the following. See the following `Block port_ranges`.
        """
        return pulumi.get(self, "port_ranges")

    @port_ranges.setter
    def port_ranges(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CustomRoutingEndpointTrafficPolicyPortRangeArgs']]]]):
        pulumi.set(self, "port_ranges", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the Custom Routing Endpoint Traffic Policy.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class CustomRoutingEndpointTrafficPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address: Optional[pulumi.Input[str]] = None,
                 endpoint_id: Optional[pulumi.Input[str]] = None,
                 port_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CustomRoutingEndpointTrafficPolicyPortRangeArgs']]]]] = None,
                 __props__=None):
        """
        Provides a Global Accelerator (GA) Custom Routing Endpoint Traffic Policy resource.

        For information about Global Accelerator (GA) Custom Routing Endpoint Traffic Policy and how to use it, see [What is Custom Routing Endpoint Traffic Policy](https://www.alibabacloud.com/help/en/global-accelerator/latest/createcustomroutingendpointtrafficpolicies).

        > **NOTE:** Available in v1.197.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.ga.CustomRoutingEndpointTrafficPolicy("default",
            address="192.168.192.2",
            endpoint_id="your_custom_routing_endpoint_id",
            port_ranges=[alicloud.ga.CustomRoutingEndpointTrafficPolicyPortRangeArgs(
                from_port=10001,
                to_port=10002,
            )])
        ```

        ## Import

        Global Accelerator (GA) Custom Routing Endpoint Traffic Policy can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:ga/customRoutingEndpointTrafficPolicy:CustomRoutingEndpointTrafficPolicy example <endpoint_id>:<custom_routing_endpoint_traffic_policy_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address: The IP address of the destination to which traffic is allowed.
        :param pulumi.Input[str] endpoint_id: The ID of the Custom Routing Endpoint.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CustomRoutingEndpointTrafficPolicyPortRangeArgs']]]] port_ranges: Port rangeSee the following. See the following `Block port_ranges`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CustomRoutingEndpointTrafficPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Global Accelerator (GA) Custom Routing Endpoint Traffic Policy resource.

        For information about Global Accelerator (GA) Custom Routing Endpoint Traffic Policy and how to use it, see [What is Custom Routing Endpoint Traffic Policy](https://www.alibabacloud.com/help/en/global-accelerator/latest/createcustomroutingendpointtrafficpolicies).

        > **NOTE:** Available in v1.197.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.ga.CustomRoutingEndpointTrafficPolicy("default",
            address="192.168.192.2",
            endpoint_id="your_custom_routing_endpoint_id",
            port_ranges=[alicloud.ga.CustomRoutingEndpointTrafficPolicyPortRangeArgs(
                from_port=10001,
                to_port=10002,
            )])
        ```

        ## Import

        Global Accelerator (GA) Custom Routing Endpoint Traffic Policy can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:ga/customRoutingEndpointTrafficPolicy:CustomRoutingEndpointTrafficPolicy example <endpoint_id>:<custom_routing_endpoint_traffic_policy_id>
        ```

        :param str resource_name: The name of the resource.
        :param CustomRoutingEndpointTrafficPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CustomRoutingEndpointTrafficPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address: Optional[pulumi.Input[str]] = None,
                 endpoint_id: Optional[pulumi.Input[str]] = None,
                 port_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CustomRoutingEndpointTrafficPolicyPortRangeArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CustomRoutingEndpointTrafficPolicyArgs.__new__(CustomRoutingEndpointTrafficPolicyArgs)

            if address is None and not opts.urn:
                raise TypeError("Missing required property 'address'")
            __props__.__dict__["address"] = address
            if endpoint_id is None and not opts.urn:
                raise TypeError("Missing required property 'endpoint_id'")
            __props__.__dict__["endpoint_id"] = endpoint_id
            __props__.__dict__["port_ranges"] = port_ranges
            __props__.__dict__["accelerator_id"] = None
            __props__.__dict__["custom_routing_endpoint_traffic_policy_id"] = None
            __props__.__dict__["endpoint_group_id"] = None
            __props__.__dict__["listener_id"] = None
            __props__.__dict__["status"] = None
        super(CustomRoutingEndpointTrafficPolicy, __self__).__init__(
            'alicloud:ga/customRoutingEndpointTrafficPolicy:CustomRoutingEndpointTrafficPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            accelerator_id: Optional[pulumi.Input[str]] = None,
            address: Optional[pulumi.Input[str]] = None,
            custom_routing_endpoint_traffic_policy_id: Optional[pulumi.Input[str]] = None,
            endpoint_group_id: Optional[pulumi.Input[str]] = None,
            endpoint_id: Optional[pulumi.Input[str]] = None,
            listener_id: Optional[pulumi.Input[str]] = None,
            port_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CustomRoutingEndpointTrafficPolicyPortRangeArgs']]]]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'CustomRoutingEndpointTrafficPolicy':
        """
        Get an existing CustomRoutingEndpointTrafficPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accelerator_id: The ID of the GA instance.
        :param pulumi.Input[str] address: The IP address of the destination to which traffic is allowed.
        :param pulumi.Input[str] custom_routing_endpoint_traffic_policy_id: The ID of the Custom Routing Endpoint Traffic Policy.
        :param pulumi.Input[str] endpoint_group_id: The ID of the endpoint group.
        :param pulumi.Input[str] endpoint_id: The ID of the Custom Routing Endpoint.
        :param pulumi.Input[str] listener_id: The ID of the listener.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CustomRoutingEndpointTrafficPolicyPortRangeArgs']]]] port_ranges: Port rangeSee the following. See the following `Block port_ranges`.
        :param pulumi.Input[str] status: The status of the Custom Routing Endpoint Traffic Policy.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CustomRoutingEndpointTrafficPolicyState.__new__(_CustomRoutingEndpointTrafficPolicyState)

        __props__.__dict__["accelerator_id"] = accelerator_id
        __props__.__dict__["address"] = address
        __props__.__dict__["custom_routing_endpoint_traffic_policy_id"] = custom_routing_endpoint_traffic_policy_id
        __props__.__dict__["endpoint_group_id"] = endpoint_group_id
        __props__.__dict__["endpoint_id"] = endpoint_id
        __props__.__dict__["listener_id"] = listener_id
        __props__.__dict__["port_ranges"] = port_ranges
        __props__.__dict__["status"] = status
        return CustomRoutingEndpointTrafficPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="acceleratorId")
    def accelerator_id(self) -> pulumi.Output[str]:
        """
        The ID of the GA instance.
        """
        return pulumi.get(self, "accelerator_id")

    @property
    @pulumi.getter
    def address(self) -> pulumi.Output[str]:
        """
        The IP address of the destination to which traffic is allowed.
        """
        return pulumi.get(self, "address")

    @property
    @pulumi.getter(name="customRoutingEndpointTrafficPolicyId")
    def custom_routing_endpoint_traffic_policy_id(self) -> pulumi.Output[str]:
        """
        The ID of the Custom Routing Endpoint Traffic Policy.
        """
        return pulumi.get(self, "custom_routing_endpoint_traffic_policy_id")

    @property
    @pulumi.getter(name="endpointGroupId")
    def endpoint_group_id(self) -> pulumi.Output[str]:
        """
        The ID of the endpoint group.
        """
        return pulumi.get(self, "endpoint_group_id")

    @property
    @pulumi.getter(name="endpointId")
    def endpoint_id(self) -> pulumi.Output[str]:
        """
        The ID of the Custom Routing Endpoint.
        """
        return pulumi.get(self, "endpoint_id")

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> pulumi.Output[str]:
        """
        The ID of the listener.
        """
        return pulumi.get(self, "listener_id")

    @property
    @pulumi.getter(name="portRanges")
    def port_ranges(self) -> pulumi.Output[Optional[Sequence['outputs.CustomRoutingEndpointTrafficPolicyPortRange']]]:
        """
        Port rangeSee the following. See the following `Block port_ranges`.
        """
        return pulumi.get(self, "port_ranges")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the Custom Routing Endpoint Traffic Policy.
        """
        return pulumi.get(self, "status")

