# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ListenerAclAttachmentArgs', 'ListenerAclAttachment']

@pulumi.input_type
class ListenerAclAttachmentArgs:
    def __init__(__self__, *,
                 acl_id: pulumi.Input[str],
                 acl_type: pulumi.Input[str],
                 listener_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a ListenerAclAttachment resource.
        :param pulumi.Input[str] acl_id: The ID of the Acl.
        :param pulumi.Input[str] acl_type: The type of the ACL. Valid values: 
               - White: a whitelist. Only requests from the IP addresses or CIDR blocks in the ACL are forwarded. The whitelist applies to scenarios in which you want to allow only specific IP addresses to access an application. Risks may arise if you specify an ACL as a whitelist. After a whitelist is configured, only IP addresses in the whitelist can access the Application Load Balancer (ALB) listener. If you enable a whitelist but the whitelist does not contain an IP address, the listener forwards all requests.
               - Black: a blacklist. All requests from the IP addresses or CIDR blocks in the ACL are blocked. The blacklist applies to scenarios in which you want to block access from specific IP addresses to an application. If you enable a blacklist but the blacklist does not contain an IP address, the listener forwards all requests.
        :param pulumi.Input[str] listener_id: The ID of the ALB listener.
        """
        pulumi.set(__self__, "acl_id", acl_id)
        pulumi.set(__self__, "acl_type", acl_type)
        pulumi.set(__self__, "listener_id", listener_id)

    @property
    @pulumi.getter(name="aclId")
    def acl_id(self) -> pulumi.Input[str]:
        """
        The ID of the Acl.
        """
        return pulumi.get(self, "acl_id")

    @acl_id.setter
    def acl_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "acl_id", value)

    @property
    @pulumi.getter(name="aclType")
    def acl_type(self) -> pulumi.Input[str]:
        """
        The type of the ACL. Valid values: 
        - White: a whitelist. Only requests from the IP addresses or CIDR blocks in the ACL are forwarded. The whitelist applies to scenarios in which you want to allow only specific IP addresses to access an application. Risks may arise if you specify an ACL as a whitelist. After a whitelist is configured, only IP addresses in the whitelist can access the Application Load Balancer (ALB) listener. If you enable a whitelist but the whitelist does not contain an IP address, the listener forwards all requests.
        - Black: a blacklist. All requests from the IP addresses or CIDR blocks in the ACL are blocked. The blacklist applies to scenarios in which you want to block access from specific IP addresses to an application. If you enable a blacklist but the blacklist does not contain an IP address, the listener forwards all requests.
        """
        return pulumi.get(self, "acl_type")

    @acl_type.setter
    def acl_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "acl_type", value)

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> pulumi.Input[str]:
        """
        The ID of the ALB listener.
        """
        return pulumi.get(self, "listener_id")

    @listener_id.setter
    def listener_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "listener_id", value)


@pulumi.input_type
class _ListenerAclAttachmentState:
    def __init__(__self__, *,
                 acl_id: Optional[pulumi.Input[str]] = None,
                 acl_type: Optional[pulumi.Input[str]] = None,
                 listener_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ListenerAclAttachment resources.
        :param pulumi.Input[str] acl_id: The ID of the Acl.
        :param pulumi.Input[str] acl_type: The type of the ACL. Valid values: 
               - White: a whitelist. Only requests from the IP addresses or CIDR blocks in the ACL are forwarded. The whitelist applies to scenarios in which you want to allow only specific IP addresses to access an application. Risks may arise if you specify an ACL as a whitelist. After a whitelist is configured, only IP addresses in the whitelist can access the Application Load Balancer (ALB) listener. If you enable a whitelist but the whitelist does not contain an IP address, the listener forwards all requests.
               - Black: a blacklist. All requests from the IP addresses or CIDR blocks in the ACL are blocked. The blacklist applies to scenarios in which you want to block access from specific IP addresses to an application. If you enable a blacklist but the blacklist does not contain an IP address, the listener forwards all requests.
        :param pulumi.Input[str] listener_id: The ID of the ALB listener.
        :param pulumi.Input[str] status: The status of the Listener Acl Attachment.
        """
        if acl_id is not None:
            pulumi.set(__self__, "acl_id", acl_id)
        if acl_type is not None:
            pulumi.set(__self__, "acl_type", acl_type)
        if listener_id is not None:
            pulumi.set(__self__, "listener_id", listener_id)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="aclId")
    def acl_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Acl.
        """
        return pulumi.get(self, "acl_id")

    @acl_id.setter
    def acl_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "acl_id", value)

    @property
    @pulumi.getter(name="aclType")
    def acl_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the ACL. Valid values: 
        - White: a whitelist. Only requests from the IP addresses or CIDR blocks in the ACL are forwarded. The whitelist applies to scenarios in which you want to allow only specific IP addresses to access an application. Risks may arise if you specify an ACL as a whitelist. After a whitelist is configured, only IP addresses in the whitelist can access the Application Load Balancer (ALB) listener. If you enable a whitelist but the whitelist does not contain an IP address, the listener forwards all requests.
        - Black: a blacklist. All requests from the IP addresses or CIDR blocks in the ACL are blocked. The blacklist applies to scenarios in which you want to block access from specific IP addresses to an application. If you enable a blacklist but the blacklist does not contain an IP address, the listener forwards all requests.
        """
        return pulumi.get(self, "acl_type")

    @acl_type.setter
    def acl_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "acl_type", value)

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the ALB listener.
        """
        return pulumi.get(self, "listener_id")

    @listener_id.setter
    def listener_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "listener_id", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the Listener Acl Attachment.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class ListenerAclAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 acl_id: Optional[pulumi.Input[str]] = None,
                 acl_type: Optional[pulumi.Input[str]] = None,
                 listener_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Application Load Balancer (ALB) Listener Acl Attachment resource.

        For information about Application Load Balancer (ALB) Listener Acl Attachment and how to use it, see [What is Listener Acl Attachment](https://www.alibabacloud.com/help/en/server-load-balancer/latest/associateaclswithlistener).

        > **NOTE:** Available in v1.163.0+.

        > **NOTE:** You can associate at most three ACLs with a listener.

        > **NOTE:** You can only configure either a whitelist or a blacklist for listener, not at the same time.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default_resource_groups = alicloud.resourcemanager.get_resource_groups()
        default_acl = alicloud.alb.Acl("defaultAcl",
            acl_name="example_value",
            resource_group_id=default_resource_groups.groups[0].id,
            acl_entries=[alicloud.alb.AclAclEntryArgs(
                description="description",
                entry="10.0.0.0/24",
            )])
        default_zones = alicloud.alb.get_zones()
        default_networks = alicloud.vpc.get_networks(name_regex="default-NODELETING")
        default1 = alicloud.vpc.get_switches(vpc_id=default_networks.ids[0],
            zone_id=default_zones.zones[0].id)
        default2 = alicloud.vpc.get_switches(vpc_id=default_networks.ids[0],
            zone_id=default_zones.zones[1].id)
        default_load_balancer = alicloud.alb.LoadBalancer("defaultLoadBalancer",
            vpc_id=default_networks.ids[0],
            address_type="Internet",
            address_allocated_mode="Fixed",
            load_balancer_name="example_value",
            load_balancer_edition="Standard",
            resource_group_id=default_resource_groups.groups[0].id,
            load_balancer_billing_config=alicloud.alb.LoadBalancerLoadBalancerBillingConfigArgs(
                pay_type="PayAsYouGo",
            ),
            tags={
                "Created": "TF",
            },
            zone_mappings=[
                alicloud.alb.LoadBalancerZoneMappingArgs(
                    vswitch_id=default1.ids[0],
                    zone_id=default_zones.zones[0].id,
                ),
                alicloud.alb.LoadBalancerZoneMappingArgs(
                    vswitch_id=default2.ids[0],
                    zone_id=default_zones.zones[1].id,
                ),
            ],
            modification_protection_config=alicloud.alb.LoadBalancerModificationProtectionConfigArgs(
                status="NonProtection",
            ))
        default_server_group = alicloud.alb.ServerGroup("defaultServerGroup",
            protocol="HTTP",
            vpc_id=default_networks.vpcs[0].id,
            server_group_name="example_value",
            resource_group_id=default_resource_groups.groups[0].id,
            health_check_config=alicloud.alb.ServerGroupHealthCheckConfigArgs(
                health_check_enabled=False,
            ),
            sticky_session_config=alicloud.alb.ServerGroupStickySessionConfigArgs(
                sticky_session_enabled=False,
            ),
            tags={
                "Created": "TF",
            })
        default_listener = alicloud.alb.Listener("defaultListener",
            load_balancer_id=default_load_balancer.id,
            listener_protocol="HTTP",
            listener_port=80,
            listener_description="example_value",
            default_actions=[alicloud.alb.ListenerDefaultActionArgs(
                type="ForwardGroup",
                forward_group_config=alicloud.alb.ListenerDefaultActionForwardGroupConfigArgs(
                    server_group_tuples=[alicloud.alb.ListenerDefaultActionForwardGroupConfigServerGroupTupleArgs(
                        server_group_id=default_server_group.id,
                    )],
                ),
            )])
        default_listener_acl_attachment = alicloud.alb.ListenerAclAttachment("defaultListenerAclAttachment",
            acl_id=default_acl.id,
            listener_id=default_listener.id,
            acl_type="White")
        ```

        ## Import

        Application Load Balancer (ALB) Listener Acl Attachment can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:alb/listenerAclAttachment:ListenerAclAttachment example <listener_id>:<acl_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] acl_id: The ID of the Acl.
        :param pulumi.Input[str] acl_type: The type of the ACL. Valid values: 
               - White: a whitelist. Only requests from the IP addresses or CIDR blocks in the ACL are forwarded. The whitelist applies to scenarios in which you want to allow only specific IP addresses to access an application. Risks may arise if you specify an ACL as a whitelist. After a whitelist is configured, only IP addresses in the whitelist can access the Application Load Balancer (ALB) listener. If you enable a whitelist but the whitelist does not contain an IP address, the listener forwards all requests.
               - Black: a blacklist. All requests from the IP addresses or CIDR blocks in the ACL are blocked. The blacklist applies to scenarios in which you want to block access from specific IP addresses to an application. If you enable a blacklist but the blacklist does not contain an IP address, the listener forwards all requests.
        :param pulumi.Input[str] listener_id: The ID of the ALB listener.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ListenerAclAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Application Load Balancer (ALB) Listener Acl Attachment resource.

        For information about Application Load Balancer (ALB) Listener Acl Attachment and how to use it, see [What is Listener Acl Attachment](https://www.alibabacloud.com/help/en/server-load-balancer/latest/associateaclswithlistener).

        > **NOTE:** Available in v1.163.0+.

        > **NOTE:** You can associate at most three ACLs with a listener.

        > **NOTE:** You can only configure either a whitelist or a blacklist for listener, not at the same time.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default_resource_groups = alicloud.resourcemanager.get_resource_groups()
        default_acl = alicloud.alb.Acl("defaultAcl",
            acl_name="example_value",
            resource_group_id=default_resource_groups.groups[0].id,
            acl_entries=[alicloud.alb.AclAclEntryArgs(
                description="description",
                entry="10.0.0.0/24",
            )])
        default_zones = alicloud.alb.get_zones()
        default_networks = alicloud.vpc.get_networks(name_regex="default-NODELETING")
        default1 = alicloud.vpc.get_switches(vpc_id=default_networks.ids[0],
            zone_id=default_zones.zones[0].id)
        default2 = alicloud.vpc.get_switches(vpc_id=default_networks.ids[0],
            zone_id=default_zones.zones[1].id)
        default_load_balancer = alicloud.alb.LoadBalancer("defaultLoadBalancer",
            vpc_id=default_networks.ids[0],
            address_type="Internet",
            address_allocated_mode="Fixed",
            load_balancer_name="example_value",
            load_balancer_edition="Standard",
            resource_group_id=default_resource_groups.groups[0].id,
            load_balancer_billing_config=alicloud.alb.LoadBalancerLoadBalancerBillingConfigArgs(
                pay_type="PayAsYouGo",
            ),
            tags={
                "Created": "TF",
            },
            zone_mappings=[
                alicloud.alb.LoadBalancerZoneMappingArgs(
                    vswitch_id=default1.ids[0],
                    zone_id=default_zones.zones[0].id,
                ),
                alicloud.alb.LoadBalancerZoneMappingArgs(
                    vswitch_id=default2.ids[0],
                    zone_id=default_zones.zones[1].id,
                ),
            ],
            modification_protection_config=alicloud.alb.LoadBalancerModificationProtectionConfigArgs(
                status="NonProtection",
            ))
        default_server_group = alicloud.alb.ServerGroup("defaultServerGroup",
            protocol="HTTP",
            vpc_id=default_networks.vpcs[0].id,
            server_group_name="example_value",
            resource_group_id=default_resource_groups.groups[0].id,
            health_check_config=alicloud.alb.ServerGroupHealthCheckConfigArgs(
                health_check_enabled=False,
            ),
            sticky_session_config=alicloud.alb.ServerGroupStickySessionConfigArgs(
                sticky_session_enabled=False,
            ),
            tags={
                "Created": "TF",
            })
        default_listener = alicloud.alb.Listener("defaultListener",
            load_balancer_id=default_load_balancer.id,
            listener_protocol="HTTP",
            listener_port=80,
            listener_description="example_value",
            default_actions=[alicloud.alb.ListenerDefaultActionArgs(
                type="ForwardGroup",
                forward_group_config=alicloud.alb.ListenerDefaultActionForwardGroupConfigArgs(
                    server_group_tuples=[alicloud.alb.ListenerDefaultActionForwardGroupConfigServerGroupTupleArgs(
                        server_group_id=default_server_group.id,
                    )],
                ),
            )])
        default_listener_acl_attachment = alicloud.alb.ListenerAclAttachment("defaultListenerAclAttachment",
            acl_id=default_acl.id,
            listener_id=default_listener.id,
            acl_type="White")
        ```

        ## Import

        Application Load Balancer (ALB) Listener Acl Attachment can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:alb/listenerAclAttachment:ListenerAclAttachment example <listener_id>:<acl_id>
        ```

        :param str resource_name: The name of the resource.
        :param ListenerAclAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ListenerAclAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 acl_id: Optional[pulumi.Input[str]] = None,
                 acl_type: Optional[pulumi.Input[str]] = None,
                 listener_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ListenerAclAttachmentArgs.__new__(ListenerAclAttachmentArgs)

            if acl_id is None and not opts.urn:
                raise TypeError("Missing required property 'acl_id'")
            __props__.__dict__["acl_id"] = acl_id
            if acl_type is None and not opts.urn:
                raise TypeError("Missing required property 'acl_type'")
            __props__.__dict__["acl_type"] = acl_type
            if listener_id is None and not opts.urn:
                raise TypeError("Missing required property 'listener_id'")
            __props__.__dict__["listener_id"] = listener_id
            __props__.__dict__["status"] = None
        super(ListenerAclAttachment, __self__).__init__(
            'alicloud:alb/listenerAclAttachment:ListenerAclAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            acl_id: Optional[pulumi.Input[str]] = None,
            acl_type: Optional[pulumi.Input[str]] = None,
            listener_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'ListenerAclAttachment':
        """
        Get an existing ListenerAclAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] acl_id: The ID of the Acl.
        :param pulumi.Input[str] acl_type: The type of the ACL. Valid values: 
               - White: a whitelist. Only requests from the IP addresses or CIDR blocks in the ACL are forwarded. The whitelist applies to scenarios in which you want to allow only specific IP addresses to access an application. Risks may arise if you specify an ACL as a whitelist. After a whitelist is configured, only IP addresses in the whitelist can access the Application Load Balancer (ALB) listener. If you enable a whitelist but the whitelist does not contain an IP address, the listener forwards all requests.
               - Black: a blacklist. All requests from the IP addresses or CIDR blocks in the ACL are blocked. The blacklist applies to scenarios in which you want to block access from specific IP addresses to an application. If you enable a blacklist but the blacklist does not contain an IP address, the listener forwards all requests.
        :param pulumi.Input[str] listener_id: The ID of the ALB listener.
        :param pulumi.Input[str] status: The status of the Listener Acl Attachment.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ListenerAclAttachmentState.__new__(_ListenerAclAttachmentState)

        __props__.__dict__["acl_id"] = acl_id
        __props__.__dict__["acl_type"] = acl_type
        __props__.__dict__["listener_id"] = listener_id
        __props__.__dict__["status"] = status
        return ListenerAclAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="aclId")
    def acl_id(self) -> pulumi.Output[str]:
        """
        The ID of the Acl.
        """
        return pulumi.get(self, "acl_id")

    @property
    @pulumi.getter(name="aclType")
    def acl_type(self) -> pulumi.Output[str]:
        """
        The type of the ACL. Valid values: 
        - White: a whitelist. Only requests from the IP addresses or CIDR blocks in the ACL are forwarded. The whitelist applies to scenarios in which you want to allow only specific IP addresses to access an application. Risks may arise if you specify an ACL as a whitelist. After a whitelist is configured, only IP addresses in the whitelist can access the Application Load Balancer (ALB) listener. If you enable a whitelist but the whitelist does not contain an IP address, the listener forwards all requests.
        - Black: a blacklist. All requests from the IP addresses or CIDR blocks in the ACL are blocked. The blacklist applies to scenarios in which you want to block access from specific IP addresses to an application. If you enable a blacklist but the blacklist does not contain an IP address, the listener forwards all requests.
        """
        return pulumi.get(self, "acl_type")

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> pulumi.Output[str]:
        """
        The ID of the ALB listener.
        """
        return pulumi.get(self, "listener_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the Listener Acl Attachment.
        """
        return pulumi.get(self, "status")

