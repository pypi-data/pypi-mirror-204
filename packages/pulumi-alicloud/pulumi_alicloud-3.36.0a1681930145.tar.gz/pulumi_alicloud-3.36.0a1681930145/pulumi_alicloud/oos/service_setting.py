# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ServiceSettingArgs', 'ServiceSetting']

@pulumi.input_type
class ServiceSettingArgs:
    def __init__(__self__, *,
                 delivery_oss_bucket_name: Optional[pulumi.Input[str]] = None,
                 delivery_oss_enabled: Optional[pulumi.Input[bool]] = None,
                 delivery_oss_key_prefix: Optional[pulumi.Input[str]] = None,
                 delivery_sls_enabled: Optional[pulumi.Input[bool]] = None,
                 delivery_sls_project_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ServiceSetting resource.
        :param pulumi.Input[str] delivery_oss_bucket_name: The name of the OSS bucket. **NOTE:** When the `delivery_oss_enabled` is `true`, The `delivery_oss_bucket_name` is valid.
        :param pulumi.Input[bool] delivery_oss_enabled: Is the recording function for the OSS delivery template enabled.
        :param pulumi.Input[str] delivery_oss_key_prefix: The Directory of the OSS bucket. **NOTE:** When the `delivery_oss_enabled` is `true`, The `delivery_oss_bucket_name` is valid.
        :param pulumi.Input[bool] delivery_sls_enabled: Is the execution record function to SLS delivery Template turned on.
        :param pulumi.Input[str] delivery_sls_project_name: The name of SLS  Project. **NOTE:** When the `delivery_sls_enabled` is `true`, The `delivery_sls_project_name` is valid.
        """
        if delivery_oss_bucket_name is not None:
            pulumi.set(__self__, "delivery_oss_bucket_name", delivery_oss_bucket_name)
        if delivery_oss_enabled is not None:
            pulumi.set(__self__, "delivery_oss_enabled", delivery_oss_enabled)
        if delivery_oss_key_prefix is not None:
            pulumi.set(__self__, "delivery_oss_key_prefix", delivery_oss_key_prefix)
        if delivery_sls_enabled is not None:
            pulumi.set(__self__, "delivery_sls_enabled", delivery_sls_enabled)
        if delivery_sls_project_name is not None:
            pulumi.set(__self__, "delivery_sls_project_name", delivery_sls_project_name)

    @property
    @pulumi.getter(name="deliveryOssBucketName")
    def delivery_oss_bucket_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the OSS bucket. **NOTE:** When the `delivery_oss_enabled` is `true`, The `delivery_oss_bucket_name` is valid.
        """
        return pulumi.get(self, "delivery_oss_bucket_name")

    @delivery_oss_bucket_name.setter
    def delivery_oss_bucket_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "delivery_oss_bucket_name", value)

    @property
    @pulumi.getter(name="deliveryOssEnabled")
    def delivery_oss_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the recording function for the OSS delivery template enabled.
        """
        return pulumi.get(self, "delivery_oss_enabled")

    @delivery_oss_enabled.setter
    def delivery_oss_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delivery_oss_enabled", value)

    @property
    @pulumi.getter(name="deliveryOssKeyPrefix")
    def delivery_oss_key_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        The Directory of the OSS bucket. **NOTE:** When the `delivery_oss_enabled` is `true`, The `delivery_oss_bucket_name` is valid.
        """
        return pulumi.get(self, "delivery_oss_key_prefix")

    @delivery_oss_key_prefix.setter
    def delivery_oss_key_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "delivery_oss_key_prefix", value)

    @property
    @pulumi.getter(name="deliverySlsEnabled")
    def delivery_sls_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the execution record function to SLS delivery Template turned on.
        """
        return pulumi.get(self, "delivery_sls_enabled")

    @delivery_sls_enabled.setter
    def delivery_sls_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delivery_sls_enabled", value)

    @property
    @pulumi.getter(name="deliverySlsProjectName")
    def delivery_sls_project_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of SLS  Project. **NOTE:** When the `delivery_sls_enabled` is `true`, The `delivery_sls_project_name` is valid.
        """
        return pulumi.get(self, "delivery_sls_project_name")

    @delivery_sls_project_name.setter
    def delivery_sls_project_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "delivery_sls_project_name", value)


@pulumi.input_type
class _ServiceSettingState:
    def __init__(__self__, *,
                 delivery_oss_bucket_name: Optional[pulumi.Input[str]] = None,
                 delivery_oss_enabled: Optional[pulumi.Input[bool]] = None,
                 delivery_oss_key_prefix: Optional[pulumi.Input[str]] = None,
                 delivery_sls_enabled: Optional[pulumi.Input[bool]] = None,
                 delivery_sls_project_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ServiceSetting resources.
        :param pulumi.Input[str] delivery_oss_bucket_name: The name of the OSS bucket. **NOTE:** When the `delivery_oss_enabled` is `true`, The `delivery_oss_bucket_name` is valid.
        :param pulumi.Input[bool] delivery_oss_enabled: Is the recording function for the OSS delivery template enabled.
        :param pulumi.Input[str] delivery_oss_key_prefix: The Directory of the OSS bucket. **NOTE:** When the `delivery_oss_enabled` is `true`, The `delivery_oss_bucket_name` is valid.
        :param pulumi.Input[bool] delivery_sls_enabled: Is the execution record function to SLS delivery Template turned on.
        :param pulumi.Input[str] delivery_sls_project_name: The name of SLS  Project. **NOTE:** When the `delivery_sls_enabled` is `true`, The `delivery_sls_project_name` is valid.
        """
        if delivery_oss_bucket_name is not None:
            pulumi.set(__self__, "delivery_oss_bucket_name", delivery_oss_bucket_name)
        if delivery_oss_enabled is not None:
            pulumi.set(__self__, "delivery_oss_enabled", delivery_oss_enabled)
        if delivery_oss_key_prefix is not None:
            pulumi.set(__self__, "delivery_oss_key_prefix", delivery_oss_key_prefix)
        if delivery_sls_enabled is not None:
            pulumi.set(__self__, "delivery_sls_enabled", delivery_sls_enabled)
        if delivery_sls_project_name is not None:
            pulumi.set(__self__, "delivery_sls_project_name", delivery_sls_project_name)

    @property
    @pulumi.getter(name="deliveryOssBucketName")
    def delivery_oss_bucket_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the OSS bucket. **NOTE:** When the `delivery_oss_enabled` is `true`, The `delivery_oss_bucket_name` is valid.
        """
        return pulumi.get(self, "delivery_oss_bucket_name")

    @delivery_oss_bucket_name.setter
    def delivery_oss_bucket_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "delivery_oss_bucket_name", value)

    @property
    @pulumi.getter(name="deliveryOssEnabled")
    def delivery_oss_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the recording function for the OSS delivery template enabled.
        """
        return pulumi.get(self, "delivery_oss_enabled")

    @delivery_oss_enabled.setter
    def delivery_oss_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delivery_oss_enabled", value)

    @property
    @pulumi.getter(name="deliveryOssKeyPrefix")
    def delivery_oss_key_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        The Directory of the OSS bucket. **NOTE:** When the `delivery_oss_enabled` is `true`, The `delivery_oss_bucket_name` is valid.
        """
        return pulumi.get(self, "delivery_oss_key_prefix")

    @delivery_oss_key_prefix.setter
    def delivery_oss_key_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "delivery_oss_key_prefix", value)

    @property
    @pulumi.getter(name="deliverySlsEnabled")
    def delivery_sls_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the execution record function to SLS delivery Template turned on.
        """
        return pulumi.get(self, "delivery_sls_enabled")

    @delivery_sls_enabled.setter
    def delivery_sls_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delivery_sls_enabled", value)

    @property
    @pulumi.getter(name="deliverySlsProjectName")
    def delivery_sls_project_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of SLS  Project. **NOTE:** When the `delivery_sls_enabled` is `true`, The `delivery_sls_project_name` is valid.
        """
        return pulumi.get(self, "delivery_sls_project_name")

    @delivery_sls_project_name.setter
    def delivery_sls_project_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "delivery_sls_project_name", value)


class ServiceSetting(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 delivery_oss_bucket_name: Optional[pulumi.Input[str]] = None,
                 delivery_oss_enabled: Optional[pulumi.Input[bool]] = None,
                 delivery_oss_key_prefix: Optional[pulumi.Input[str]] = None,
                 delivery_sls_enabled: Optional[pulumi.Input[bool]] = None,
                 delivery_sls_project_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a OOS Service Setting resource.

        For information about OOS Service Setting and how to use it, see [What is Service Setting](https://www.alibabacloud.com/help/en/doc-detail/268700.html).

        > **NOTE:** Available in v1.147.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf-testaccoossetting"
        default_bucket = alicloud.oss.Bucket("defaultBucket",
            bucket=name,
            acl="public-read-write")
        default_project = alicloud.log.Project("defaultProject")
        default_service_setting = alicloud.oos.ServiceSetting("defaultServiceSetting",
            delivery_oss_enabled=True,
            delivery_oss_key_prefix="path1/",
            delivery_oss_bucket_name=default_bucket.bucket,
            delivery_sls_enabled=True,
            delivery_sls_project_name=default_project.name)
        ```

        ## Import

        OOS Service Setting can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:oos/serviceSetting:ServiceSetting example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] delivery_oss_bucket_name: The name of the OSS bucket. **NOTE:** When the `delivery_oss_enabled` is `true`, The `delivery_oss_bucket_name` is valid.
        :param pulumi.Input[bool] delivery_oss_enabled: Is the recording function for the OSS delivery template enabled.
        :param pulumi.Input[str] delivery_oss_key_prefix: The Directory of the OSS bucket. **NOTE:** When the `delivery_oss_enabled` is `true`, The `delivery_oss_bucket_name` is valid.
        :param pulumi.Input[bool] delivery_sls_enabled: Is the execution record function to SLS delivery Template turned on.
        :param pulumi.Input[str] delivery_sls_project_name: The name of SLS  Project. **NOTE:** When the `delivery_sls_enabled` is `true`, The `delivery_sls_project_name` is valid.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ServiceSettingArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a OOS Service Setting resource.

        For information about OOS Service Setting and how to use it, see [What is Service Setting](https://www.alibabacloud.com/help/en/doc-detail/268700.html).

        > **NOTE:** Available in v1.147.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf-testaccoossetting"
        default_bucket = alicloud.oss.Bucket("defaultBucket",
            bucket=name,
            acl="public-read-write")
        default_project = alicloud.log.Project("defaultProject")
        default_service_setting = alicloud.oos.ServiceSetting("defaultServiceSetting",
            delivery_oss_enabled=True,
            delivery_oss_key_prefix="path1/",
            delivery_oss_bucket_name=default_bucket.bucket,
            delivery_sls_enabled=True,
            delivery_sls_project_name=default_project.name)
        ```

        ## Import

        OOS Service Setting can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:oos/serviceSetting:ServiceSetting example <id>
        ```

        :param str resource_name: The name of the resource.
        :param ServiceSettingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceSettingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 delivery_oss_bucket_name: Optional[pulumi.Input[str]] = None,
                 delivery_oss_enabled: Optional[pulumi.Input[bool]] = None,
                 delivery_oss_key_prefix: Optional[pulumi.Input[str]] = None,
                 delivery_sls_enabled: Optional[pulumi.Input[bool]] = None,
                 delivery_sls_project_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServiceSettingArgs.__new__(ServiceSettingArgs)

            __props__.__dict__["delivery_oss_bucket_name"] = delivery_oss_bucket_name
            __props__.__dict__["delivery_oss_enabled"] = delivery_oss_enabled
            __props__.__dict__["delivery_oss_key_prefix"] = delivery_oss_key_prefix
            __props__.__dict__["delivery_sls_enabled"] = delivery_sls_enabled
            __props__.__dict__["delivery_sls_project_name"] = delivery_sls_project_name
        super(ServiceSetting, __self__).__init__(
            'alicloud:oos/serviceSetting:ServiceSetting',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            delivery_oss_bucket_name: Optional[pulumi.Input[str]] = None,
            delivery_oss_enabled: Optional[pulumi.Input[bool]] = None,
            delivery_oss_key_prefix: Optional[pulumi.Input[str]] = None,
            delivery_sls_enabled: Optional[pulumi.Input[bool]] = None,
            delivery_sls_project_name: Optional[pulumi.Input[str]] = None) -> 'ServiceSetting':
        """
        Get an existing ServiceSetting resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] delivery_oss_bucket_name: The name of the OSS bucket. **NOTE:** When the `delivery_oss_enabled` is `true`, The `delivery_oss_bucket_name` is valid.
        :param pulumi.Input[bool] delivery_oss_enabled: Is the recording function for the OSS delivery template enabled.
        :param pulumi.Input[str] delivery_oss_key_prefix: The Directory of the OSS bucket. **NOTE:** When the `delivery_oss_enabled` is `true`, The `delivery_oss_bucket_name` is valid.
        :param pulumi.Input[bool] delivery_sls_enabled: Is the execution record function to SLS delivery Template turned on.
        :param pulumi.Input[str] delivery_sls_project_name: The name of SLS  Project. **NOTE:** When the `delivery_sls_enabled` is `true`, The `delivery_sls_project_name` is valid.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServiceSettingState.__new__(_ServiceSettingState)

        __props__.__dict__["delivery_oss_bucket_name"] = delivery_oss_bucket_name
        __props__.__dict__["delivery_oss_enabled"] = delivery_oss_enabled
        __props__.__dict__["delivery_oss_key_prefix"] = delivery_oss_key_prefix
        __props__.__dict__["delivery_sls_enabled"] = delivery_sls_enabled
        __props__.__dict__["delivery_sls_project_name"] = delivery_sls_project_name
        return ServiceSetting(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="deliveryOssBucketName")
    def delivery_oss_bucket_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the OSS bucket. **NOTE:** When the `delivery_oss_enabled` is `true`, The `delivery_oss_bucket_name` is valid.
        """
        return pulumi.get(self, "delivery_oss_bucket_name")

    @property
    @pulumi.getter(name="deliveryOssEnabled")
    def delivery_oss_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Is the recording function for the OSS delivery template enabled.
        """
        return pulumi.get(self, "delivery_oss_enabled")

    @property
    @pulumi.getter(name="deliveryOssKeyPrefix")
    def delivery_oss_key_prefix(self) -> pulumi.Output[Optional[str]]:
        """
        The Directory of the OSS bucket. **NOTE:** When the `delivery_oss_enabled` is `true`, The `delivery_oss_bucket_name` is valid.
        """
        return pulumi.get(self, "delivery_oss_key_prefix")

    @property
    @pulumi.getter(name="deliverySlsEnabled")
    def delivery_sls_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Is the execution record function to SLS delivery Template turned on.
        """
        return pulumi.get(self, "delivery_sls_enabled")

    @property
    @pulumi.getter(name="deliverySlsProjectName")
    def delivery_sls_project_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of SLS  Project. **NOTE:** When the `delivery_sls_enabled` is `true`, The `delivery_sls_project_name` is valid.
        """
        return pulumi.get(self, "delivery_sls_project_name")

