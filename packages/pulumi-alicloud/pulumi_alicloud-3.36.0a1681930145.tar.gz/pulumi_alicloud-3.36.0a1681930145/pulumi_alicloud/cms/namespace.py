# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['NamespaceArgs', 'Namespace']

@pulumi.input_type
class NamespaceArgs:
    def __init__(__self__, *,
                 namespace: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 specification: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Namespace resource.
        :param pulumi.Input[str] namespace: Indicator warehouse name. The namespace can contain lowercase letters, digits, and hyphens (-).
        :param pulumi.Input[str] description: Description of indicator warehouse.
        :param pulumi.Input[str] specification: Data storage duration. Valid values: `cms.s1.12xlarge`, `cms.s1.2xlarge`, `cms.s1.3xlarge`, `cms.s1.6xlarge`, `cms.s1.large`, `cms.s1.xlarge`. 
               - `cms.s1.large`: Data storage duration is 15 days.
               - `cms.s1.xlarge`: Data storage duration is 32 days.
               - `cms.s1.2xlarge`: Data storage duration 63 days.
               - `cms.s1.3xlarge`: (Default) Data storage duration 93 days.
               - `cms.s1.6xlarge`: Data storage duration 185 days.
               - `cms.s1.12xlarge`: Data storage duration 376 days.
        """
        pulumi.set(__self__, "namespace", namespace)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if specification is not None:
            pulumi.set(__self__, "specification", specification)

    @property
    @pulumi.getter
    def namespace(self) -> pulumi.Input[str]:
        """
        Indicator warehouse name. The namespace can contain lowercase letters, digits, and hyphens (-).
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: pulumi.Input[str]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of indicator warehouse.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def specification(self) -> Optional[pulumi.Input[str]]:
        """
        Data storage duration. Valid values: `cms.s1.12xlarge`, `cms.s1.2xlarge`, `cms.s1.3xlarge`, `cms.s1.6xlarge`, `cms.s1.large`, `cms.s1.xlarge`. 
        - `cms.s1.large`: Data storage duration is 15 days.
        - `cms.s1.xlarge`: Data storage duration is 32 days.
        - `cms.s1.2xlarge`: Data storage duration 63 days.
        - `cms.s1.3xlarge`: (Default) Data storage duration 93 days.
        - `cms.s1.6xlarge`: Data storage duration 185 days.
        - `cms.s1.12xlarge`: Data storage duration 376 days.
        """
        return pulumi.get(self, "specification")

    @specification.setter
    def specification(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "specification", value)


@pulumi.input_type
class _NamespaceState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 specification: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Namespace resources.
        :param pulumi.Input[str] description: Description of indicator warehouse.
        :param pulumi.Input[str] namespace: Indicator warehouse name. The namespace can contain lowercase letters, digits, and hyphens (-).
        :param pulumi.Input[str] specification: Data storage duration. Valid values: `cms.s1.12xlarge`, `cms.s1.2xlarge`, `cms.s1.3xlarge`, `cms.s1.6xlarge`, `cms.s1.large`, `cms.s1.xlarge`. 
               - `cms.s1.large`: Data storage duration is 15 days.
               - `cms.s1.xlarge`: Data storage duration is 32 days.
               - `cms.s1.2xlarge`: Data storage duration 63 days.
               - `cms.s1.3xlarge`: (Default) Data storage duration 93 days.
               - `cms.s1.6xlarge`: Data storage duration 185 days.
               - `cms.s1.12xlarge`: Data storage duration 376 days.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if specification is not None:
            pulumi.set(__self__, "specification", specification)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of indicator warehouse.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        Indicator warehouse name. The namespace can contain lowercase letters, digits, and hyphens (-).
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter
    def specification(self) -> Optional[pulumi.Input[str]]:
        """
        Data storage duration. Valid values: `cms.s1.12xlarge`, `cms.s1.2xlarge`, `cms.s1.3xlarge`, `cms.s1.6xlarge`, `cms.s1.large`, `cms.s1.xlarge`. 
        - `cms.s1.large`: Data storage duration is 15 days.
        - `cms.s1.xlarge`: Data storage duration is 32 days.
        - `cms.s1.2xlarge`: Data storage duration 63 days.
        - `cms.s1.3xlarge`: (Default) Data storage duration 93 days.
        - `cms.s1.6xlarge`: Data storage duration 185 days.
        - `cms.s1.12xlarge`: Data storage duration 376 days.
        """
        return pulumi.get(self, "specification")

    @specification.setter
    def specification(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "specification", value)


class Namespace(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 specification: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Cloud Monitor Service Namespace resource.

        For information about Cloud Monitor Service Namespace and how to use it, see [What is Namespace](https://www.alibabacloud.com/help/doc-detail/28608.htm).

        > **NOTE:** Available in v1.171.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example = alicloud.cms.Namespace("example",
            namespace="example-value",
            specification="cms.s1.large")
        ```

        ## Import

        Cloud Monitor Service Namespace can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cms/namespace:Namespace example <namespace>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of indicator warehouse.
        :param pulumi.Input[str] namespace: Indicator warehouse name. The namespace can contain lowercase letters, digits, and hyphens (-).
        :param pulumi.Input[str] specification: Data storage duration. Valid values: `cms.s1.12xlarge`, `cms.s1.2xlarge`, `cms.s1.3xlarge`, `cms.s1.6xlarge`, `cms.s1.large`, `cms.s1.xlarge`. 
               - `cms.s1.large`: Data storage duration is 15 days.
               - `cms.s1.xlarge`: Data storage duration is 32 days.
               - `cms.s1.2xlarge`: Data storage duration 63 days.
               - `cms.s1.3xlarge`: (Default) Data storage duration 93 days.
               - `cms.s1.6xlarge`: Data storage duration 185 days.
               - `cms.s1.12xlarge`: Data storage duration 376 days.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NamespaceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Cloud Monitor Service Namespace resource.

        For information about Cloud Monitor Service Namespace and how to use it, see [What is Namespace](https://www.alibabacloud.com/help/doc-detail/28608.htm).

        > **NOTE:** Available in v1.171.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example = alicloud.cms.Namespace("example",
            namespace="example-value",
            specification="cms.s1.large")
        ```

        ## Import

        Cloud Monitor Service Namespace can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cms/namespace:Namespace example <namespace>
        ```

        :param str resource_name: The name of the resource.
        :param NamespaceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NamespaceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 specification: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NamespaceArgs.__new__(NamespaceArgs)

            __props__.__dict__["description"] = description
            if namespace is None and not opts.urn:
                raise TypeError("Missing required property 'namespace'")
            __props__.__dict__["namespace"] = namespace
            __props__.__dict__["specification"] = specification
        super(Namespace, __self__).__init__(
            'alicloud:cms/namespace:Namespace',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            namespace: Optional[pulumi.Input[str]] = None,
            specification: Optional[pulumi.Input[str]] = None) -> 'Namespace':
        """
        Get an existing Namespace resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of indicator warehouse.
        :param pulumi.Input[str] namespace: Indicator warehouse name. The namespace can contain lowercase letters, digits, and hyphens (-).
        :param pulumi.Input[str] specification: Data storage duration. Valid values: `cms.s1.12xlarge`, `cms.s1.2xlarge`, `cms.s1.3xlarge`, `cms.s1.6xlarge`, `cms.s1.large`, `cms.s1.xlarge`. 
               - `cms.s1.large`: Data storage duration is 15 days.
               - `cms.s1.xlarge`: Data storage duration is 32 days.
               - `cms.s1.2xlarge`: Data storage duration 63 days.
               - `cms.s1.3xlarge`: (Default) Data storage duration 93 days.
               - `cms.s1.6xlarge`: Data storage duration 185 days.
               - `cms.s1.12xlarge`: Data storage duration 376 days.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NamespaceState.__new__(_NamespaceState)

        __props__.__dict__["description"] = description
        __props__.__dict__["namespace"] = namespace
        __props__.__dict__["specification"] = specification
        return Namespace(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of indicator warehouse.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def namespace(self) -> pulumi.Output[str]:
        """
        Indicator warehouse name. The namespace can contain lowercase letters, digits, and hyphens (-).
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter
    def specification(self) -> pulumi.Output[str]:
        """
        Data storage duration. Valid values: `cms.s1.12xlarge`, `cms.s1.2xlarge`, `cms.s1.3xlarge`, `cms.s1.6xlarge`, `cms.s1.large`, `cms.s1.xlarge`. 
        - `cms.s1.large`: Data storage duration is 15 days.
        - `cms.s1.xlarge`: Data storage duration is 32 days.
        - `cms.s1.2xlarge`: Data storage duration 63 days.
        - `cms.s1.3xlarge`: (Default) Data storage duration 93 days.
        - `cms.s1.6xlarge`: Data storage duration 185 days.
        - `cms.s1.12xlarge`: Data storage duration 376 days.
        """
        return pulumi.get(self, "specification")

