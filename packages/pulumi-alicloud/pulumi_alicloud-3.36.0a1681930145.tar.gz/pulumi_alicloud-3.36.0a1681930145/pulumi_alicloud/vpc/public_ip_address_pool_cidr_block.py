# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['PublicIpAddressPoolCidrBlockArgs', 'PublicIpAddressPoolCidrBlock']

@pulumi.input_type
class PublicIpAddressPoolCidrBlockArgs:
    def __init__(__self__, *,
                 cidr_block: pulumi.Input[str],
                 public_ip_address_pool_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a PublicIpAddressPoolCidrBlock resource.
        :param pulumi.Input[str] cidr_block: The CIDR block.
        :param pulumi.Input[str] public_ip_address_pool_id: The ID of the VPC Public IP address pool.
        """
        pulumi.set(__self__, "cidr_block", cidr_block)
        pulumi.set(__self__, "public_ip_address_pool_id", public_ip_address_pool_id)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> pulumi.Input[str]:
        """
        The CIDR block.
        """
        return pulumi.get(self, "cidr_block")

    @cidr_block.setter
    def cidr_block(self, value: pulumi.Input[str]):
        pulumi.set(self, "cidr_block", value)

    @property
    @pulumi.getter(name="publicIpAddressPoolId")
    def public_ip_address_pool_id(self) -> pulumi.Input[str]:
        """
        The ID of the VPC Public IP address pool.
        """
        return pulumi.get(self, "public_ip_address_pool_id")

    @public_ip_address_pool_id.setter
    def public_ip_address_pool_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "public_ip_address_pool_id", value)


@pulumi.input_type
class _PublicIpAddressPoolCidrBlockState:
    def __init__(__self__, *,
                 cidr_block: Optional[pulumi.Input[str]] = None,
                 public_ip_address_pool_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering PublicIpAddressPoolCidrBlock resources.
        :param pulumi.Input[str] cidr_block: The CIDR block.
        :param pulumi.Input[str] public_ip_address_pool_id: The ID of the VPC Public IP address pool.
        :param pulumi.Input[str] status: The status of the VPC Public Ip Address Pool Cidr Block.
        """
        if cidr_block is not None:
            pulumi.set(__self__, "cidr_block", cidr_block)
        if public_ip_address_pool_id is not None:
            pulumi.set(__self__, "public_ip_address_pool_id", public_ip_address_pool_id)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> Optional[pulumi.Input[str]]:
        """
        The CIDR block.
        """
        return pulumi.get(self, "cidr_block")

    @cidr_block.setter
    def cidr_block(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cidr_block", value)

    @property
    @pulumi.getter(name="publicIpAddressPoolId")
    def public_ip_address_pool_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the VPC Public IP address pool.
        """
        return pulumi.get(self, "public_ip_address_pool_id")

    @public_ip_address_pool_id.setter
    def public_ip_address_pool_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_ip_address_pool_id", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the VPC Public Ip Address Pool Cidr Block.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class PublicIpAddressPoolCidrBlock(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cidr_block: Optional[pulumi.Input[str]] = None,
                 public_ip_address_pool_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a VPC Public Ip Address Pool Cidr Block resource.

        For information about VPC Public Ip Address Pool Cidr Block and how to use it, see [What is Public Ip Address Pool Cidr Block](https://www.alibabacloud.com/help/en/virtual-private-cloud/latest/429100).

        > **NOTE:** Available in v1.189.0+.

        > **NOTE:** Only users who have the required permissions can use the IP address pool feature of Elastic IP Address (EIP). To apply for the required permissions, [submit a ticket](https://smartservice.console.aliyun.com/service/create-ticket).

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default_public_ip_address_pool = alicloud.vpc.PublicIpAddressPool("defaultPublicIpAddressPool",
            public_ip_address_pool_name="example_value",
            isp="BGP",
            description="example_value")
        default_public_ip_address_pool_cidr_block = alicloud.vpc.PublicIpAddressPoolCidrBlock("defaultPublicIpAddressPoolCidrBlock",
            public_ip_address_pool_id=default_public_ip_address_pool.id,
            cidr_block="your_cidr_block")
        ```

        ## Import

        VPC Public Ip Address Pool Cidr Block can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:vpc/publicIpAddressPoolCidrBlock:PublicIpAddressPoolCidrBlock example <public_ip_address_pool_id>:<cidr_block>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cidr_block: The CIDR block.
        :param pulumi.Input[str] public_ip_address_pool_id: The ID of the VPC Public IP address pool.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PublicIpAddressPoolCidrBlockArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a VPC Public Ip Address Pool Cidr Block resource.

        For information about VPC Public Ip Address Pool Cidr Block and how to use it, see [What is Public Ip Address Pool Cidr Block](https://www.alibabacloud.com/help/en/virtual-private-cloud/latest/429100).

        > **NOTE:** Available in v1.189.0+.

        > **NOTE:** Only users who have the required permissions can use the IP address pool feature of Elastic IP Address (EIP). To apply for the required permissions, [submit a ticket](https://smartservice.console.aliyun.com/service/create-ticket).

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default_public_ip_address_pool = alicloud.vpc.PublicIpAddressPool("defaultPublicIpAddressPool",
            public_ip_address_pool_name="example_value",
            isp="BGP",
            description="example_value")
        default_public_ip_address_pool_cidr_block = alicloud.vpc.PublicIpAddressPoolCidrBlock("defaultPublicIpAddressPoolCidrBlock",
            public_ip_address_pool_id=default_public_ip_address_pool.id,
            cidr_block="your_cidr_block")
        ```

        ## Import

        VPC Public Ip Address Pool Cidr Block can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:vpc/publicIpAddressPoolCidrBlock:PublicIpAddressPoolCidrBlock example <public_ip_address_pool_id>:<cidr_block>
        ```

        :param str resource_name: The name of the resource.
        :param PublicIpAddressPoolCidrBlockArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PublicIpAddressPoolCidrBlockArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cidr_block: Optional[pulumi.Input[str]] = None,
                 public_ip_address_pool_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PublicIpAddressPoolCidrBlockArgs.__new__(PublicIpAddressPoolCidrBlockArgs)

            if cidr_block is None and not opts.urn:
                raise TypeError("Missing required property 'cidr_block'")
            __props__.__dict__["cidr_block"] = cidr_block
            if public_ip_address_pool_id is None and not opts.urn:
                raise TypeError("Missing required property 'public_ip_address_pool_id'")
            __props__.__dict__["public_ip_address_pool_id"] = public_ip_address_pool_id
            __props__.__dict__["status"] = None
        super(PublicIpAddressPoolCidrBlock, __self__).__init__(
            'alicloud:vpc/publicIpAddressPoolCidrBlock:PublicIpAddressPoolCidrBlock',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cidr_block: Optional[pulumi.Input[str]] = None,
            public_ip_address_pool_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'PublicIpAddressPoolCidrBlock':
        """
        Get an existing PublicIpAddressPoolCidrBlock resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cidr_block: The CIDR block.
        :param pulumi.Input[str] public_ip_address_pool_id: The ID of the VPC Public IP address pool.
        :param pulumi.Input[str] status: The status of the VPC Public Ip Address Pool Cidr Block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PublicIpAddressPoolCidrBlockState.__new__(_PublicIpAddressPoolCidrBlockState)

        __props__.__dict__["cidr_block"] = cidr_block
        __props__.__dict__["public_ip_address_pool_id"] = public_ip_address_pool_id
        __props__.__dict__["status"] = status
        return PublicIpAddressPoolCidrBlock(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> pulumi.Output[str]:
        """
        The CIDR block.
        """
        return pulumi.get(self, "cidr_block")

    @property
    @pulumi.getter(name="publicIpAddressPoolId")
    def public_ip_address_pool_id(self) -> pulumi.Output[str]:
        """
        The ID of the VPC Public IP address pool.
        """
        return pulumi.get(self, "public_ip_address_pool_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the VPC Public Ip Address Pool Cidr Block.
        """
        return pulumi.get(self, "status")

