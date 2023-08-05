# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['StorageBundleArgs', 'StorageBundle']

@pulumi.input_type
class StorageBundleArgs:
    def __init__(__self__, *,
                 storage_bundle_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a StorageBundle resource.
        :param pulumi.Input[str] storage_bundle_name: The name of storage bundle.
        :param pulumi.Input[str] description: The description of storage bundle.
        """
        pulumi.set(__self__, "storage_bundle_name", storage_bundle_name)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter(name="storageBundleName")
    def storage_bundle_name(self) -> pulumi.Input[str]:
        """
        The name of storage bundle.
        """
        return pulumi.get(self, "storage_bundle_name")

    @storage_bundle_name.setter
    def storage_bundle_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "storage_bundle_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of storage bundle.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class _StorageBundleState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 storage_bundle_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering StorageBundle resources.
        :param pulumi.Input[str] description: The description of storage bundle.
        :param pulumi.Input[str] storage_bundle_name: The name of storage bundle.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if storage_bundle_name is not None:
            pulumi.set(__self__, "storage_bundle_name", storage_bundle_name)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of storage bundle.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="storageBundleName")
    def storage_bundle_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of storage bundle.
        """
        return pulumi.get(self, "storage_bundle_name")

    @storage_bundle_name.setter
    def storage_bundle_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_bundle_name", value)


class StorageBundle(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 storage_bundle_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Cloud Storage Gateway Storage Bundle resource.

        For information about Cloud Storage Gateway Storage Bundle and how to use it, see [What is Storage Bundle](https://www.alibabacloud.com/help/en/doc-detail/53972.htm).

        > **NOTE:** Available in v1.116.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example = alicloud.cloudstoragegateway.StorageBundle("example", storage_bundle_name="example_value")
        ```

        ## Import

        Cloud Storage Gateway Storage Bundle can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cloudstoragegateway/storageBundle:StorageBundle example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of storage bundle.
        :param pulumi.Input[str] storage_bundle_name: The name of storage bundle.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StorageBundleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Cloud Storage Gateway Storage Bundle resource.

        For information about Cloud Storage Gateway Storage Bundle and how to use it, see [What is Storage Bundle](https://www.alibabacloud.com/help/en/doc-detail/53972.htm).

        > **NOTE:** Available in v1.116.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example = alicloud.cloudstoragegateway.StorageBundle("example", storage_bundle_name="example_value")
        ```

        ## Import

        Cloud Storage Gateway Storage Bundle can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cloudstoragegateway/storageBundle:StorageBundle example <id>
        ```

        :param str resource_name: The name of the resource.
        :param StorageBundleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StorageBundleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 storage_bundle_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = StorageBundleArgs.__new__(StorageBundleArgs)

            __props__.__dict__["description"] = description
            if storage_bundle_name is None and not opts.urn:
                raise TypeError("Missing required property 'storage_bundle_name'")
            __props__.__dict__["storage_bundle_name"] = storage_bundle_name
        super(StorageBundle, __self__).__init__(
            'alicloud:cloudstoragegateway/storageBundle:StorageBundle',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            storage_bundle_name: Optional[pulumi.Input[str]] = None) -> 'StorageBundle':
        """
        Get an existing StorageBundle resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of storage bundle.
        :param pulumi.Input[str] storage_bundle_name: The name of storage bundle.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _StorageBundleState.__new__(_StorageBundleState)

        __props__.__dict__["description"] = description
        __props__.__dict__["storage_bundle_name"] = storage_bundle_name
        return StorageBundle(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of storage bundle.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="storageBundleName")
    def storage_bundle_name(self) -> pulumi.Output[str]:
        """
        The name of storage bundle.
        """
        return pulumi.get(self, "storage_bundle_name")

