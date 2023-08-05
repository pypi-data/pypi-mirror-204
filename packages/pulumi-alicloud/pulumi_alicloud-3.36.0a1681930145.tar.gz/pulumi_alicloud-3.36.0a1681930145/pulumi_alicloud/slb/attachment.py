# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AttachmentArgs', 'Attachment']

@pulumi.input_type
class AttachmentArgs:
    def __init__(__self__, *,
                 instance_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 load_balancer_id: pulumi.Input[str],
                 backend_servers: Optional[pulumi.Input[str]] = None,
                 delete_protection_validation: Optional[pulumi.Input[bool]] = None,
                 server_type: Optional[pulumi.Input[str]] = None,
                 weight: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a Attachment resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] instance_ids: A list of instance ids to added backend server in the SLB.
        :param pulumi.Input[str] load_balancer_id: ID of the load balancer.
        :param pulumi.Input[str] backend_servers: The backend servers of the load balancer.
        :param pulumi.Input[bool] delete_protection_validation: Checking DeleteProtection of SLB instance before deleting. If true, this resource will not be deleted when its SLB instance enabled DeleteProtection. Default to false.
        :param pulumi.Input[str] server_type: Type of the instances. Valid value ecs, eni. Default to ecs.
        :param pulumi.Input[int] weight: Weight of the instances. Valid value range: [0-100]. Default to 100.
        """
        pulumi.set(__self__, "instance_ids", instance_ids)
        pulumi.set(__self__, "load_balancer_id", load_balancer_id)
        if backend_servers is not None:
            pulumi.set(__self__, "backend_servers", backend_servers)
        if delete_protection_validation is not None:
            pulumi.set(__self__, "delete_protection_validation", delete_protection_validation)
        if server_type is not None:
            pulumi.set(__self__, "server_type", server_type)
        if weight is not None:
            pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter(name="instanceIds")
    def instance_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of instance ids to added backend server in the SLB.
        """
        return pulumi.get(self, "instance_ids")

    @instance_ids.setter
    def instance_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "instance_ids", value)

    @property
    @pulumi.getter(name="loadBalancerId")
    def load_balancer_id(self) -> pulumi.Input[str]:
        """
        ID of the load balancer.
        """
        return pulumi.get(self, "load_balancer_id")

    @load_balancer_id.setter
    def load_balancer_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "load_balancer_id", value)

    @property
    @pulumi.getter(name="backendServers")
    def backend_servers(self) -> Optional[pulumi.Input[str]]:
        """
        The backend servers of the load balancer.
        """
        return pulumi.get(self, "backend_servers")

    @backend_servers.setter
    def backend_servers(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backend_servers", value)

    @property
    @pulumi.getter(name="deleteProtectionValidation")
    def delete_protection_validation(self) -> Optional[pulumi.Input[bool]]:
        """
        Checking DeleteProtection of SLB instance before deleting. If true, this resource will not be deleted when its SLB instance enabled DeleteProtection. Default to false.
        """
        return pulumi.get(self, "delete_protection_validation")

    @delete_protection_validation.setter
    def delete_protection_validation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delete_protection_validation", value)

    @property
    @pulumi.getter(name="serverType")
    def server_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of the instances. Valid value ecs, eni. Default to ecs.
        """
        return pulumi.get(self, "server_type")

    @server_type.setter
    def server_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_type", value)

    @property
    @pulumi.getter
    def weight(self) -> Optional[pulumi.Input[int]]:
        """
        Weight of the instances. Valid value range: [0-100]. Default to 100.
        """
        return pulumi.get(self, "weight")

    @weight.setter
    def weight(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "weight", value)


@pulumi.input_type
class _AttachmentState:
    def __init__(__self__, *,
                 backend_servers: Optional[pulumi.Input[str]] = None,
                 delete_protection_validation: Optional[pulumi.Input[bool]] = None,
                 instance_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 load_balancer_id: Optional[pulumi.Input[str]] = None,
                 server_type: Optional[pulumi.Input[str]] = None,
                 weight: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering Attachment resources.
        :param pulumi.Input[str] backend_servers: The backend servers of the load balancer.
        :param pulumi.Input[bool] delete_protection_validation: Checking DeleteProtection of SLB instance before deleting. If true, this resource will not be deleted when its SLB instance enabled DeleteProtection. Default to false.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] instance_ids: A list of instance ids to added backend server in the SLB.
        :param pulumi.Input[str] load_balancer_id: ID of the load balancer.
        :param pulumi.Input[str] server_type: Type of the instances. Valid value ecs, eni. Default to ecs.
        :param pulumi.Input[int] weight: Weight of the instances. Valid value range: [0-100]. Default to 100.
        """
        if backend_servers is not None:
            pulumi.set(__self__, "backend_servers", backend_servers)
        if delete_protection_validation is not None:
            pulumi.set(__self__, "delete_protection_validation", delete_protection_validation)
        if instance_ids is not None:
            pulumi.set(__self__, "instance_ids", instance_ids)
        if load_balancer_id is not None:
            pulumi.set(__self__, "load_balancer_id", load_balancer_id)
        if server_type is not None:
            pulumi.set(__self__, "server_type", server_type)
        if weight is not None:
            pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter(name="backendServers")
    def backend_servers(self) -> Optional[pulumi.Input[str]]:
        """
        The backend servers of the load balancer.
        """
        return pulumi.get(self, "backend_servers")

    @backend_servers.setter
    def backend_servers(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backend_servers", value)

    @property
    @pulumi.getter(name="deleteProtectionValidation")
    def delete_protection_validation(self) -> Optional[pulumi.Input[bool]]:
        """
        Checking DeleteProtection of SLB instance before deleting. If true, this resource will not be deleted when its SLB instance enabled DeleteProtection. Default to false.
        """
        return pulumi.get(self, "delete_protection_validation")

    @delete_protection_validation.setter
    def delete_protection_validation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delete_protection_validation", value)

    @property
    @pulumi.getter(name="instanceIds")
    def instance_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of instance ids to added backend server in the SLB.
        """
        return pulumi.get(self, "instance_ids")

    @instance_ids.setter
    def instance_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "instance_ids", value)

    @property
    @pulumi.getter(name="loadBalancerId")
    def load_balancer_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the load balancer.
        """
        return pulumi.get(self, "load_balancer_id")

    @load_balancer_id.setter
    def load_balancer_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "load_balancer_id", value)

    @property
    @pulumi.getter(name="serverType")
    def server_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of the instances. Valid value ecs, eni. Default to ecs.
        """
        return pulumi.get(self, "server_type")

    @server_type.setter
    def server_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_type", value)

    @property
    @pulumi.getter
    def weight(self) -> Optional[pulumi.Input[int]]:
        """
        Weight of the instances. Valid value range: [0-100]. Default to 100.
        """
        return pulumi.get(self, "weight")

    @weight.setter
    def weight(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "weight", value)


class Attachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend_servers: Optional[pulumi.Input[str]] = None,
                 delete_protection_validation: Optional[pulumi.Input[bool]] = None,
                 instance_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 load_balancer_id: Optional[pulumi.Input[str]] = None,
                 server_type: Optional[pulumi.Input[str]] = None,
                 weight: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "slbattachmenttest"
        default_zones = alicloud.get_zones(available_disk_category="cloud_efficiency",
            available_resource_creation="VSwitch")
        default_instance_types = alicloud.ecs.get_instance_types(availability_zone=default_zones.zones[0].id,
            cpu_core_count=1,
            memory_size=2)
        default_images = alicloud.ecs.get_images(name_regex="^ubuntu_18.*64",
            most_recent=True,
            owners="system")
        default_network = alicloud.vpc.Network("defaultNetwork", cidr_block="172.16.0.0/16")
        default_switch = alicloud.vpc.Switch("defaultSwitch",
            vpc_id=default_network.id,
            cidr_block="172.16.0.0/16",
            zone_id=default_zones.zones[0].id,
            vswitch_name=name)
        default_security_group = alicloud.ecs.SecurityGroup("defaultSecurityGroup", vpc_id=default_network.id)
        default_instance = alicloud.ecs.Instance("defaultInstance",
            image_id=default_images.images[0].id,
            instance_type=default_instance_types.instance_types[0].id,
            internet_charge_type="PayByTraffic",
            internet_max_bandwidth_out=5,
            system_disk_category="cloud_efficiency",
            security_groups=[default_security_group.id],
            instance_name=name,
            vswitch_id=default_switch.id)
        default_application_load_balancer = alicloud.slb.ApplicationLoadBalancer("defaultApplicationLoadBalancer",
            load_balancer_name=name,
            vswitch_id=default_switch.id)
        default_attachment = alicloud.slb.Attachment("defaultAttachment",
            load_balancer_id=default_application_load_balancer.id,
            instance_ids=[default_instance.id],
            weight=90)
        ```

        ## Import

        Load balancer attachment can be imported using the id or load balancer id, e.g.

        ```sh
         $ pulumi import alicloud:slb/attachment:Attachment example lb-abc123456
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backend_servers: The backend servers of the load balancer.
        :param pulumi.Input[bool] delete_protection_validation: Checking DeleteProtection of SLB instance before deleting. If true, this resource will not be deleted when its SLB instance enabled DeleteProtection. Default to false.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] instance_ids: A list of instance ids to added backend server in the SLB.
        :param pulumi.Input[str] load_balancer_id: ID of the load balancer.
        :param pulumi.Input[str] server_type: Type of the instances. Valid value ecs, eni. Default to ecs.
        :param pulumi.Input[int] weight: Weight of the instances. Valid value range: [0-100]. Default to 100.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "slbattachmenttest"
        default_zones = alicloud.get_zones(available_disk_category="cloud_efficiency",
            available_resource_creation="VSwitch")
        default_instance_types = alicloud.ecs.get_instance_types(availability_zone=default_zones.zones[0].id,
            cpu_core_count=1,
            memory_size=2)
        default_images = alicloud.ecs.get_images(name_regex="^ubuntu_18.*64",
            most_recent=True,
            owners="system")
        default_network = alicloud.vpc.Network("defaultNetwork", cidr_block="172.16.0.0/16")
        default_switch = alicloud.vpc.Switch("defaultSwitch",
            vpc_id=default_network.id,
            cidr_block="172.16.0.0/16",
            zone_id=default_zones.zones[0].id,
            vswitch_name=name)
        default_security_group = alicloud.ecs.SecurityGroup("defaultSecurityGroup", vpc_id=default_network.id)
        default_instance = alicloud.ecs.Instance("defaultInstance",
            image_id=default_images.images[0].id,
            instance_type=default_instance_types.instance_types[0].id,
            internet_charge_type="PayByTraffic",
            internet_max_bandwidth_out=5,
            system_disk_category="cloud_efficiency",
            security_groups=[default_security_group.id],
            instance_name=name,
            vswitch_id=default_switch.id)
        default_application_load_balancer = alicloud.slb.ApplicationLoadBalancer("defaultApplicationLoadBalancer",
            load_balancer_name=name,
            vswitch_id=default_switch.id)
        default_attachment = alicloud.slb.Attachment("defaultAttachment",
            load_balancer_id=default_application_load_balancer.id,
            instance_ids=[default_instance.id],
            weight=90)
        ```

        ## Import

        Load balancer attachment can be imported using the id or load balancer id, e.g.

        ```sh
         $ pulumi import alicloud:slb/attachment:Attachment example lb-abc123456
        ```

        :param str resource_name: The name of the resource.
        :param AttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend_servers: Optional[pulumi.Input[str]] = None,
                 delete_protection_validation: Optional[pulumi.Input[bool]] = None,
                 instance_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 load_balancer_id: Optional[pulumi.Input[str]] = None,
                 server_type: Optional[pulumi.Input[str]] = None,
                 weight: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AttachmentArgs.__new__(AttachmentArgs)

            __props__.__dict__["backend_servers"] = backend_servers
            __props__.__dict__["delete_protection_validation"] = delete_protection_validation
            if instance_ids is None and not opts.urn:
                raise TypeError("Missing required property 'instance_ids'")
            __props__.__dict__["instance_ids"] = instance_ids
            if load_balancer_id is None and not opts.urn:
                raise TypeError("Missing required property 'load_balancer_id'")
            __props__.__dict__["load_balancer_id"] = load_balancer_id
            __props__.__dict__["server_type"] = server_type
            __props__.__dict__["weight"] = weight
        super(Attachment, __self__).__init__(
            'alicloud:slb/attachment:Attachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            backend_servers: Optional[pulumi.Input[str]] = None,
            delete_protection_validation: Optional[pulumi.Input[bool]] = None,
            instance_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            load_balancer_id: Optional[pulumi.Input[str]] = None,
            server_type: Optional[pulumi.Input[str]] = None,
            weight: Optional[pulumi.Input[int]] = None) -> 'Attachment':
        """
        Get an existing Attachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backend_servers: The backend servers of the load balancer.
        :param pulumi.Input[bool] delete_protection_validation: Checking DeleteProtection of SLB instance before deleting. If true, this resource will not be deleted when its SLB instance enabled DeleteProtection. Default to false.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] instance_ids: A list of instance ids to added backend server in the SLB.
        :param pulumi.Input[str] load_balancer_id: ID of the load balancer.
        :param pulumi.Input[str] server_type: Type of the instances. Valid value ecs, eni. Default to ecs.
        :param pulumi.Input[int] weight: Weight of the instances. Valid value range: [0-100]. Default to 100.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AttachmentState.__new__(_AttachmentState)

        __props__.__dict__["backend_servers"] = backend_servers
        __props__.__dict__["delete_protection_validation"] = delete_protection_validation
        __props__.__dict__["instance_ids"] = instance_ids
        __props__.__dict__["load_balancer_id"] = load_balancer_id
        __props__.__dict__["server_type"] = server_type
        __props__.__dict__["weight"] = weight
        return Attachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="backendServers")
    def backend_servers(self) -> pulumi.Output[str]:
        """
        The backend servers of the load balancer.
        """
        return pulumi.get(self, "backend_servers")

    @property
    @pulumi.getter(name="deleteProtectionValidation")
    def delete_protection_validation(self) -> pulumi.Output[Optional[bool]]:
        """
        Checking DeleteProtection of SLB instance before deleting. If true, this resource will not be deleted when its SLB instance enabled DeleteProtection. Default to false.
        """
        return pulumi.get(self, "delete_protection_validation")

    @property
    @pulumi.getter(name="instanceIds")
    def instance_ids(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of instance ids to added backend server in the SLB.
        """
        return pulumi.get(self, "instance_ids")

    @property
    @pulumi.getter(name="loadBalancerId")
    def load_balancer_id(self) -> pulumi.Output[str]:
        """
        ID of the load balancer.
        """
        return pulumi.get(self, "load_balancer_id")

    @property
    @pulumi.getter(name="serverType")
    def server_type(self) -> pulumi.Output[Optional[str]]:
        """
        Type of the instances. Valid value ecs, eni. Default to ecs.
        """
        return pulumi.get(self, "server_type")

    @property
    @pulumi.getter
    def weight(self) -> pulumi.Output[Optional[int]]:
        """
        Weight of the instances. Valid value range: [0-100]. Default to 100.
        """
        return pulumi.get(self, "weight")

