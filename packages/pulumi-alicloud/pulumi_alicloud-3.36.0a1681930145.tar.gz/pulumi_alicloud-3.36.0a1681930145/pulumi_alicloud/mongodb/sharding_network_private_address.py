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

__all__ = ['ShardingNetworkPrivateAddressArgs', 'ShardingNetworkPrivateAddress']

@pulumi.input_type
class ShardingNetworkPrivateAddressArgs:
    def __init__(__self__, *,
                 db_instance_id: pulumi.Input[str],
                 node_id: pulumi.Input[str],
                 zone_id: pulumi.Input[str],
                 account_name: Optional[pulumi.Input[str]] = None,
                 account_password: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ShardingNetworkPrivateAddress resource.
        :param pulumi.Input[str] db_instance_id: The db instance id.
        :param pulumi.Input[str] node_id: The ID of the Shard node or the ConfigServer node.
        :param pulumi.Input[str] zone_id: The zone ID of the instance.
        :param pulumi.Input[str] account_name: The name of the account. 
               - The name must be 4 to 16 characters in length and can contain lowercase letters, digits, and underscores (_). It must start with a lowercase letter.
               - You need to set the account name and password only when you apply for an endpoint for a shard or Configserver node for the first time. In this case, the account name and password are used for all shard and Configserver nodes.
               - The permissions of this account are fixed to read-only.
        :param pulumi.Input[str] account_password: Account password. 
               - The password must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters. Special characters include `!#$%^&*()_+-=`.
               - The password must be 8 to 32 characters in length.
        """
        pulumi.set(__self__, "db_instance_id", db_instance_id)
        pulumi.set(__self__, "node_id", node_id)
        pulumi.set(__self__, "zone_id", zone_id)
        if account_name is not None:
            pulumi.set(__self__, "account_name", account_name)
        if account_password is not None:
            pulumi.set(__self__, "account_password", account_password)

    @property
    @pulumi.getter(name="dbInstanceId")
    def db_instance_id(self) -> pulumi.Input[str]:
        """
        The db instance id.
        """
        return pulumi.get(self, "db_instance_id")

    @db_instance_id.setter
    def db_instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "db_instance_id", value)

    @property
    @pulumi.getter(name="nodeId")
    def node_id(self) -> pulumi.Input[str]:
        """
        The ID of the Shard node or the ConfigServer node.
        """
        return pulumi.get(self, "node_id")

    @node_id.setter
    def node_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "node_id", value)

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> pulumi.Input[str]:
        """
        The zone ID of the instance.
        """
        return pulumi.get(self, "zone_id")

    @zone_id.setter
    def zone_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "zone_id", value)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the account. 
        - The name must be 4 to 16 characters in length and can contain lowercase letters, digits, and underscores (_). It must start with a lowercase letter.
        - You need to set the account name and password only when you apply for an endpoint for a shard or Configserver node for the first time. In this case, the account name and password are used for all shard and Configserver nodes.
        - The permissions of this account are fixed to read-only.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="accountPassword")
    def account_password(self) -> Optional[pulumi.Input[str]]:
        """
        Account password. 
        - The password must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters. Special characters include `!#$%^&*()_+-=`.
        - The password must be 8 to 32 characters in length.
        """
        return pulumi.get(self, "account_password")

    @account_password.setter
    def account_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_password", value)


@pulumi.input_type
class _ShardingNetworkPrivateAddressState:
    def __init__(__self__, *,
                 account_name: Optional[pulumi.Input[str]] = None,
                 account_password: Optional[pulumi.Input[str]] = None,
                 db_instance_id: Optional[pulumi.Input[str]] = None,
                 network_addresses: Optional[pulumi.Input[Sequence[pulumi.Input['ShardingNetworkPrivateAddressNetworkAddressArgs']]]] = None,
                 node_id: Optional[pulumi.Input[str]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ShardingNetworkPrivateAddress resources.
        :param pulumi.Input[str] account_name: The name of the account. 
               - The name must be 4 to 16 characters in length and can contain lowercase letters, digits, and underscores (_). It must start with a lowercase letter.
               - You need to set the account name and password only when you apply for an endpoint for a shard or Configserver node for the first time. In this case, the account name and password are used for all shard and Configserver nodes.
               - The permissions of this account are fixed to read-only.
        :param pulumi.Input[str] account_password: Account password. 
               - The password must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters. Special characters include `!#$%^&*()_+-=`.
               - The password must be 8 to 32 characters in length.
        :param pulumi.Input[str] db_instance_id: The db instance id.
        :param pulumi.Input[Sequence[pulumi.Input['ShardingNetworkPrivateAddressNetworkAddressArgs']]] network_addresses: The endpoint of the instance.
        :param pulumi.Input[str] node_id: The ID of the Shard node or the ConfigServer node.
        :param pulumi.Input[str] zone_id: The zone ID of the instance.
        """
        if account_name is not None:
            pulumi.set(__self__, "account_name", account_name)
        if account_password is not None:
            pulumi.set(__self__, "account_password", account_password)
        if db_instance_id is not None:
            pulumi.set(__self__, "db_instance_id", db_instance_id)
        if network_addresses is not None:
            pulumi.set(__self__, "network_addresses", network_addresses)
        if node_id is not None:
            pulumi.set(__self__, "node_id", node_id)
        if zone_id is not None:
            pulumi.set(__self__, "zone_id", zone_id)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the account. 
        - The name must be 4 to 16 characters in length and can contain lowercase letters, digits, and underscores (_). It must start with a lowercase letter.
        - You need to set the account name and password only when you apply for an endpoint for a shard or Configserver node for the first time. In this case, the account name and password are used for all shard and Configserver nodes.
        - The permissions of this account are fixed to read-only.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="accountPassword")
    def account_password(self) -> Optional[pulumi.Input[str]]:
        """
        Account password. 
        - The password must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters. Special characters include `!#$%^&*()_+-=`.
        - The password must be 8 to 32 characters in length.
        """
        return pulumi.get(self, "account_password")

    @account_password.setter
    def account_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_password", value)

    @property
    @pulumi.getter(name="dbInstanceId")
    def db_instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The db instance id.
        """
        return pulumi.get(self, "db_instance_id")

    @db_instance_id.setter
    def db_instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "db_instance_id", value)

    @property
    @pulumi.getter(name="networkAddresses")
    def network_addresses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ShardingNetworkPrivateAddressNetworkAddressArgs']]]]:
        """
        The endpoint of the instance.
        """
        return pulumi.get(self, "network_addresses")

    @network_addresses.setter
    def network_addresses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ShardingNetworkPrivateAddressNetworkAddressArgs']]]]):
        pulumi.set(self, "network_addresses", value)

    @property
    @pulumi.getter(name="nodeId")
    def node_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Shard node or the ConfigServer node.
        """
        return pulumi.get(self, "node_id")

    @node_id.setter
    def node_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "node_id", value)

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        The zone ID of the instance.
        """
        return pulumi.get(self, "zone_id")

    @zone_id.setter
    def zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone_id", value)


class ShardingNetworkPrivateAddress(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 account_password: Optional[pulumi.Input[str]] = None,
                 db_instance_id: Optional[pulumi.Input[str]] = None,
                 node_id: Optional[pulumi.Input[str]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a MongoDB Sharding Network Private Address resource.

        For information about MongoDB Sharding Network Private Address and how to use it, see [What is Sharding Network Private Address](https://www.alibabacloud.com/help/en/doc-detail/141403.html).

        > **NOTE:** Available in v1.157.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf-example"
        default_zones = alicloud.mongodb.get_zones()
        default_networks = alicloud.vpc.get_networks(name_regex="default-NODELETING")
        default_switches = alicloud.vpc.get_switches(vpc_id=default_networks.ids[0],
            zone_id=default_zones.zones[0].id)
        default_sharding_instance = alicloud.mongodb.ShardingInstance("defaultShardingInstance",
            zone_id=default_zones.zones[0].id,
            vswitch_id=default_switches.ids[0],
            engine_version="4.2",
            mongo_lists=[
                alicloud.mongodb.ShardingInstanceMongoListArgs(
                    node_class="dds.mongos.mid",
                ),
                alicloud.mongodb.ShardingInstanceMongoListArgs(
                    node_class="dds.mongos.mid",
                ),
            ],
            shard_lists=[
                alicloud.mongodb.ShardingInstanceShardListArgs(
                    node_class="dds.shard.mid",
                    node_storage=10,
                ),
                alicloud.mongodb.ShardingInstanceShardListArgs(
                    node_class="dds.shard.mid",
                    node_storage=10,
                ),
            ])
        example = alicloud.mongodb.ShardingNetworkPrivateAddress("example",
            db_instance_id=default_sharding_instance.id,
            node_id=default_sharding_instance.shard_lists[0].node_id,
            zone_id=default_sharding_instance.zone_id,
            account_name="example_value",
            account_password="YourPassword+12345")
        ```

        ## Import

        MongoDB Sharding Network Private Address can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:mongodb/shardingNetworkPrivateAddress:ShardingNetworkPrivateAddress example <db_instance_id>:<node_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the account. 
               - The name must be 4 to 16 characters in length and can contain lowercase letters, digits, and underscores (_). It must start with a lowercase letter.
               - You need to set the account name and password only when you apply for an endpoint for a shard or Configserver node for the first time. In this case, the account name and password are used for all shard and Configserver nodes.
               - The permissions of this account are fixed to read-only.
        :param pulumi.Input[str] account_password: Account password. 
               - The password must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters. Special characters include `!#$%^&*()_+-=`.
               - The password must be 8 to 32 characters in length.
        :param pulumi.Input[str] db_instance_id: The db instance id.
        :param pulumi.Input[str] node_id: The ID of the Shard node or the ConfigServer node.
        :param pulumi.Input[str] zone_id: The zone ID of the instance.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ShardingNetworkPrivateAddressArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a MongoDB Sharding Network Private Address resource.

        For information about MongoDB Sharding Network Private Address and how to use it, see [What is Sharding Network Private Address](https://www.alibabacloud.com/help/en/doc-detail/141403.html).

        > **NOTE:** Available in v1.157.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf-example"
        default_zones = alicloud.mongodb.get_zones()
        default_networks = alicloud.vpc.get_networks(name_regex="default-NODELETING")
        default_switches = alicloud.vpc.get_switches(vpc_id=default_networks.ids[0],
            zone_id=default_zones.zones[0].id)
        default_sharding_instance = alicloud.mongodb.ShardingInstance("defaultShardingInstance",
            zone_id=default_zones.zones[0].id,
            vswitch_id=default_switches.ids[0],
            engine_version="4.2",
            mongo_lists=[
                alicloud.mongodb.ShardingInstanceMongoListArgs(
                    node_class="dds.mongos.mid",
                ),
                alicloud.mongodb.ShardingInstanceMongoListArgs(
                    node_class="dds.mongos.mid",
                ),
            ],
            shard_lists=[
                alicloud.mongodb.ShardingInstanceShardListArgs(
                    node_class="dds.shard.mid",
                    node_storage=10,
                ),
                alicloud.mongodb.ShardingInstanceShardListArgs(
                    node_class="dds.shard.mid",
                    node_storage=10,
                ),
            ])
        example = alicloud.mongodb.ShardingNetworkPrivateAddress("example",
            db_instance_id=default_sharding_instance.id,
            node_id=default_sharding_instance.shard_lists[0].node_id,
            zone_id=default_sharding_instance.zone_id,
            account_name="example_value",
            account_password="YourPassword+12345")
        ```

        ## Import

        MongoDB Sharding Network Private Address can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:mongodb/shardingNetworkPrivateAddress:ShardingNetworkPrivateAddress example <db_instance_id>:<node_id>
        ```

        :param str resource_name: The name of the resource.
        :param ShardingNetworkPrivateAddressArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ShardingNetworkPrivateAddressArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 account_password: Optional[pulumi.Input[str]] = None,
                 db_instance_id: Optional[pulumi.Input[str]] = None,
                 node_id: Optional[pulumi.Input[str]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ShardingNetworkPrivateAddressArgs.__new__(ShardingNetworkPrivateAddressArgs)

            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["account_password"] = None if account_password is None else pulumi.Output.secret(account_password)
            if db_instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'db_instance_id'")
            __props__.__dict__["db_instance_id"] = db_instance_id
            if node_id is None and not opts.urn:
                raise TypeError("Missing required property 'node_id'")
            __props__.__dict__["node_id"] = node_id
            if zone_id is None and not opts.urn:
                raise TypeError("Missing required property 'zone_id'")
            __props__.__dict__["zone_id"] = zone_id
            __props__.__dict__["network_addresses"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["accountPassword"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(ShardingNetworkPrivateAddress, __self__).__init__(
            'alicloud:mongodb/shardingNetworkPrivateAddress:ShardingNetworkPrivateAddress',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_name: Optional[pulumi.Input[str]] = None,
            account_password: Optional[pulumi.Input[str]] = None,
            db_instance_id: Optional[pulumi.Input[str]] = None,
            network_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ShardingNetworkPrivateAddressNetworkAddressArgs']]]]] = None,
            node_id: Optional[pulumi.Input[str]] = None,
            zone_id: Optional[pulumi.Input[str]] = None) -> 'ShardingNetworkPrivateAddress':
        """
        Get an existing ShardingNetworkPrivateAddress resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the account. 
               - The name must be 4 to 16 characters in length and can contain lowercase letters, digits, and underscores (_). It must start with a lowercase letter.
               - You need to set the account name and password only when you apply for an endpoint for a shard or Configserver node for the first time. In this case, the account name and password are used for all shard and Configserver nodes.
               - The permissions of this account are fixed to read-only.
        :param pulumi.Input[str] account_password: Account password. 
               - The password must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters. Special characters include `!#$%^&*()_+-=`.
               - The password must be 8 to 32 characters in length.
        :param pulumi.Input[str] db_instance_id: The db instance id.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ShardingNetworkPrivateAddressNetworkAddressArgs']]]] network_addresses: The endpoint of the instance.
        :param pulumi.Input[str] node_id: The ID of the Shard node or the ConfigServer node.
        :param pulumi.Input[str] zone_id: The zone ID of the instance.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ShardingNetworkPrivateAddressState.__new__(_ShardingNetworkPrivateAddressState)

        __props__.__dict__["account_name"] = account_name
        __props__.__dict__["account_password"] = account_password
        __props__.__dict__["db_instance_id"] = db_instance_id
        __props__.__dict__["network_addresses"] = network_addresses
        __props__.__dict__["node_id"] = node_id
        __props__.__dict__["zone_id"] = zone_id
        return ShardingNetworkPrivateAddress(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the account. 
        - The name must be 4 to 16 characters in length and can contain lowercase letters, digits, and underscores (_). It must start with a lowercase letter.
        - You need to set the account name and password only when you apply for an endpoint for a shard or Configserver node for the first time. In this case, the account name and password are used for all shard and Configserver nodes.
        - The permissions of this account are fixed to read-only.
        """
        return pulumi.get(self, "account_name")

    @property
    @pulumi.getter(name="accountPassword")
    def account_password(self) -> pulumi.Output[Optional[str]]:
        """
        Account password. 
        - The password must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters. Special characters include `!#$%^&*()_+-=`.
        - The password must be 8 to 32 characters in length.
        """
        return pulumi.get(self, "account_password")

    @property
    @pulumi.getter(name="dbInstanceId")
    def db_instance_id(self) -> pulumi.Output[str]:
        """
        The db instance id.
        """
        return pulumi.get(self, "db_instance_id")

    @property
    @pulumi.getter(name="networkAddresses")
    def network_addresses(self) -> pulumi.Output[Sequence['outputs.ShardingNetworkPrivateAddressNetworkAddress']]:
        """
        The endpoint of the instance.
        """
        return pulumi.get(self, "network_addresses")

    @property
    @pulumi.getter(name="nodeId")
    def node_id(self) -> pulumi.Output[str]:
        """
        The ID of the Shard node or the ConfigServer node.
        """
        return pulumi.get(self, "node_id")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> pulumi.Output[str]:
        """
        The zone ID of the instance.
        """
        return pulumi.get(self, "zone_id")

