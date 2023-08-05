# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['EipAssociationArgs', 'EipAssociation']

@pulumi.input_type
class EipAssociationArgs:
    def __init__(__self__, *,
                 allocation_id: pulumi.Input[str],
                 instance_id: pulumi.Input[str],
                 force: Optional[pulumi.Input[bool]] = None,
                 instance_type: Optional[pulumi.Input[str]] = None,
                 private_ip_address: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a EipAssociation resource.
        :param pulumi.Input[str] allocation_id: The allocation EIP ID.
        :param pulumi.Input[str] instance_id: The ID of the ECS or SLB instance or Nat Gateway or NetworkInterface or HaVip.
        :param pulumi.Input[bool] force: When EIP is bound to a NAT gateway, and the NAT gateway adds a DNAT or SNAT entry, set it for `true` can unassociation any way. Default to `false`.
        :param pulumi.Input[str] instance_type: The type of cloud product that the eip instance to bind. Valid values: `EcsInstance`, `SlbInstance`, `Nat`, `NetworkInterface` and `HaVip`.
        :param pulumi.Input[str] private_ip_address: The private IP address in the network segment of the vswitch which has been assigned.
        """
        pulumi.set(__self__, "allocation_id", allocation_id)
        pulumi.set(__self__, "instance_id", instance_id)
        if force is not None:
            pulumi.set(__self__, "force", force)
        if instance_type is not None:
            pulumi.set(__self__, "instance_type", instance_type)
        if private_ip_address is not None:
            pulumi.set(__self__, "private_ip_address", private_ip_address)

    @property
    @pulumi.getter(name="allocationId")
    def allocation_id(self) -> pulumi.Input[str]:
        """
        The allocation EIP ID.
        """
        return pulumi.get(self, "allocation_id")

    @allocation_id.setter
    def allocation_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "allocation_id", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        """
        The ID of the ECS or SLB instance or Nat Gateway or NetworkInterface or HaVip.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter
    def force(self) -> Optional[pulumi.Input[bool]]:
        """
        When EIP is bound to a NAT gateway, and the NAT gateway adds a DNAT or SNAT entry, set it for `true` can unassociation any way. Default to `false`.
        """
        return pulumi.get(self, "force")

    @force.setter
    def force(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force", value)

    @property
    @pulumi.getter(name="instanceType")
    def instance_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of cloud product that the eip instance to bind. Valid values: `EcsInstance`, `SlbInstance`, `Nat`, `NetworkInterface` and `HaVip`.
        """
        return pulumi.get(self, "instance_type")

    @instance_type.setter
    def instance_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_type", value)

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        The private IP address in the network segment of the vswitch which has been assigned.
        """
        return pulumi.get(self, "private_ip_address")

    @private_ip_address.setter
    def private_ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_ip_address", value)


@pulumi.input_type
class _EipAssociationState:
    def __init__(__self__, *,
                 allocation_id: Optional[pulumi.Input[str]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 instance_type: Optional[pulumi.Input[str]] = None,
                 private_ip_address: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering EipAssociation resources.
        :param pulumi.Input[str] allocation_id: The allocation EIP ID.
        :param pulumi.Input[bool] force: When EIP is bound to a NAT gateway, and the NAT gateway adds a DNAT or SNAT entry, set it for `true` can unassociation any way. Default to `false`.
        :param pulumi.Input[str] instance_id: The ID of the ECS or SLB instance or Nat Gateway or NetworkInterface or HaVip.
        :param pulumi.Input[str] instance_type: The type of cloud product that the eip instance to bind. Valid values: `EcsInstance`, `SlbInstance`, `Nat`, `NetworkInterface` and `HaVip`.
        :param pulumi.Input[str] private_ip_address: The private IP address in the network segment of the vswitch which has been assigned.
        """
        if allocation_id is not None:
            pulumi.set(__self__, "allocation_id", allocation_id)
        if force is not None:
            pulumi.set(__self__, "force", force)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if instance_type is not None:
            pulumi.set(__self__, "instance_type", instance_type)
        if private_ip_address is not None:
            pulumi.set(__self__, "private_ip_address", private_ip_address)

    @property
    @pulumi.getter(name="allocationId")
    def allocation_id(self) -> Optional[pulumi.Input[str]]:
        """
        The allocation EIP ID.
        """
        return pulumi.get(self, "allocation_id")

    @allocation_id.setter
    def allocation_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "allocation_id", value)

    @property
    @pulumi.getter
    def force(self) -> Optional[pulumi.Input[bool]]:
        """
        When EIP is bound to a NAT gateway, and the NAT gateway adds a DNAT or SNAT entry, set it for `true` can unassociation any way. Default to `false`.
        """
        return pulumi.get(self, "force")

    @force.setter
    def force(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the ECS or SLB instance or Nat Gateway or NetworkInterface or HaVip.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="instanceType")
    def instance_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of cloud product that the eip instance to bind. Valid values: `EcsInstance`, `SlbInstance`, `Nat`, `NetworkInterface` and `HaVip`.
        """
        return pulumi.get(self, "instance_type")

    @instance_type.setter
    def instance_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_type", value)

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        The private IP address in the network segment of the vswitch which has been assigned.
        """
        return pulumi.get(self, "private_ip_address")

    @private_ip_address.setter
    def private_ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_ip_address", value)


class EipAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allocation_id: Optional[pulumi.Input[str]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 instance_type: Optional[pulumi.Input[str]] = None,
                 private_ip_address: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Import

        Elastic IP address association can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:ecs/eipAssociation:EipAssociation example eip-abc12345678:i-abc12355
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] allocation_id: The allocation EIP ID.
        :param pulumi.Input[bool] force: When EIP is bound to a NAT gateway, and the NAT gateway adds a DNAT or SNAT entry, set it for `true` can unassociation any way. Default to `false`.
        :param pulumi.Input[str] instance_id: The ID of the ECS or SLB instance or Nat Gateway or NetworkInterface or HaVip.
        :param pulumi.Input[str] instance_type: The type of cloud product that the eip instance to bind. Valid values: `EcsInstance`, `SlbInstance`, `Nat`, `NetworkInterface` and `HaVip`.
        :param pulumi.Input[str] private_ip_address: The private IP address in the network segment of the vswitch which has been assigned.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EipAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Import

        Elastic IP address association can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:ecs/eipAssociation:EipAssociation example eip-abc12345678:i-abc12355
        ```

        :param str resource_name: The name of the resource.
        :param EipAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EipAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allocation_id: Optional[pulumi.Input[str]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 instance_type: Optional[pulumi.Input[str]] = None,
                 private_ip_address: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EipAssociationArgs.__new__(EipAssociationArgs)

            if allocation_id is None and not opts.urn:
                raise TypeError("Missing required property 'allocation_id'")
            __props__.__dict__["allocation_id"] = allocation_id
            __props__.__dict__["force"] = force
            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            __props__.__dict__["instance_type"] = instance_type
            __props__.__dict__["private_ip_address"] = private_ip_address
        super(EipAssociation, __self__).__init__(
            'alicloud:ecs/eipAssociation:EipAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            allocation_id: Optional[pulumi.Input[str]] = None,
            force: Optional[pulumi.Input[bool]] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            instance_type: Optional[pulumi.Input[str]] = None,
            private_ip_address: Optional[pulumi.Input[str]] = None) -> 'EipAssociation':
        """
        Get an existing EipAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] allocation_id: The allocation EIP ID.
        :param pulumi.Input[bool] force: When EIP is bound to a NAT gateway, and the NAT gateway adds a DNAT or SNAT entry, set it for `true` can unassociation any way. Default to `false`.
        :param pulumi.Input[str] instance_id: The ID of the ECS or SLB instance or Nat Gateway or NetworkInterface or HaVip.
        :param pulumi.Input[str] instance_type: The type of cloud product that the eip instance to bind. Valid values: `EcsInstance`, `SlbInstance`, `Nat`, `NetworkInterface` and `HaVip`.
        :param pulumi.Input[str] private_ip_address: The private IP address in the network segment of the vswitch which has been assigned.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EipAssociationState.__new__(_EipAssociationState)

        __props__.__dict__["allocation_id"] = allocation_id
        __props__.__dict__["force"] = force
        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["instance_type"] = instance_type
        __props__.__dict__["private_ip_address"] = private_ip_address
        return EipAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allocationId")
    def allocation_id(self) -> pulumi.Output[str]:
        """
        The allocation EIP ID.
        """
        return pulumi.get(self, "allocation_id")

    @property
    @pulumi.getter
    def force(self) -> pulumi.Output[Optional[bool]]:
        """
        When EIP is bound to a NAT gateway, and the NAT gateway adds a DNAT or SNAT entry, set it for `true` can unassociation any way. Default to `false`.
        """
        return pulumi.get(self, "force")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        The ID of the ECS or SLB instance or Nat Gateway or NetworkInterface or HaVip.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="instanceType")
    def instance_type(self) -> pulumi.Output[str]:
        """
        The type of cloud product that the eip instance to bind. Valid values: `EcsInstance`, `SlbInstance`, `Nat`, `NetworkInterface` and `HaVip`.
        """
        return pulumi.get(self, "instance_type")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> pulumi.Output[str]:
        """
        The private IP address in the network segment of the vswitch which has been assigned.
        """
        return pulumi.get(self, "private_ip_address")

