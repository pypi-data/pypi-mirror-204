# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['StateConfigurationArgs', 'StateConfiguration']

@pulumi.input_type
class StateConfigurationArgs:
    def __init__(__self__, *,
                 schedule_expression: pulumi.Input[str],
                 schedule_type: pulumi.Input[str],
                 targets: pulumi.Input[str],
                 template_name: pulumi.Input[str],
                 configure_mode: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 template_version: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a StateConfiguration resource.
        :param pulumi.Input[str] schedule_expression: Timing expression.
        :param pulumi.Input[str] schedule_type: Timing type. Valid values: `rate`.
        :param pulumi.Input[str] targets: The Target resources.  This field is in the format of JSON strings. For detailed definition instructions, please refer to [Parameter](https://www.alibabacloud.com/help/en/doc-detail/120674.html).
        :param pulumi.Input[str] template_name: The name of the template.
        :param pulumi.Input[str] configure_mode: Configuration mode. Valid values: `ApplyAndAutoCorrect`, `ApplyAndMonitor`, `ApplyOnly`.
        :param pulumi.Input[str] description: The description of the resource.
        :param pulumi.Input[str] parameters: The parameter of the Template. This field is in the format of JSON strings. For detailed definition instructions, please refer to [Metadata types that are supported by a configuration list](https://www.alibabacloud.com/help/en/doc-detail/208276.html).
        :param pulumi.Input[str] resource_group_id: The ID of the resource group.
        :param pulumi.Input[Mapping[str, Any]] tags: The tag of the resource.
        :param pulumi.Input[str] template_version: The version number. If you do not specify this parameter, the system uses the latest version.
        """
        pulumi.set(__self__, "schedule_expression", schedule_expression)
        pulumi.set(__self__, "schedule_type", schedule_type)
        pulumi.set(__self__, "targets", targets)
        pulumi.set(__self__, "template_name", template_name)
        if configure_mode is not None:
            pulumi.set(__self__, "configure_mode", configure_mode)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if resource_group_id is not None:
            pulumi.set(__self__, "resource_group_id", resource_group_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if template_version is not None:
            pulumi.set(__self__, "template_version", template_version)

    @property
    @pulumi.getter(name="scheduleExpression")
    def schedule_expression(self) -> pulumi.Input[str]:
        """
        Timing expression.
        """
        return pulumi.get(self, "schedule_expression")

    @schedule_expression.setter
    def schedule_expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "schedule_expression", value)

    @property
    @pulumi.getter(name="scheduleType")
    def schedule_type(self) -> pulumi.Input[str]:
        """
        Timing type. Valid values: `rate`.
        """
        return pulumi.get(self, "schedule_type")

    @schedule_type.setter
    def schedule_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "schedule_type", value)

    @property
    @pulumi.getter
    def targets(self) -> pulumi.Input[str]:
        """
        The Target resources.  This field is in the format of JSON strings. For detailed definition instructions, please refer to [Parameter](https://www.alibabacloud.com/help/en/doc-detail/120674.html).
        """
        return pulumi.get(self, "targets")

    @targets.setter
    def targets(self, value: pulumi.Input[str]):
        pulumi.set(self, "targets", value)

    @property
    @pulumi.getter(name="templateName")
    def template_name(self) -> pulumi.Input[str]:
        """
        The name of the template.
        """
        return pulumi.get(self, "template_name")

    @template_name.setter
    def template_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "template_name", value)

    @property
    @pulumi.getter(name="configureMode")
    def configure_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Configuration mode. Valid values: `ApplyAndAutoCorrect`, `ApplyAndMonitor`, `ApplyOnly`.
        """
        return pulumi.get(self, "configure_mode")

    @configure_mode.setter
    def configure_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "configure_mode", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[str]]:
        """
        The parameter of the Template. This field is in the format of JSON strings. For detailed definition instructions, please refer to [Metadata types that are supported by a configuration list](https://www.alibabacloud.com/help/en/doc-detail/208276.html).
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the resource group.
        """
        return pulumi.get(self, "resource_group_id")

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        The tag of the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="templateVersion")
    def template_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version number. If you do not specify this parameter, the system uses the latest version.
        """
        return pulumi.get(self, "template_version")

    @template_version.setter
    def template_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_version", value)


@pulumi.input_type
class _StateConfigurationState:
    def __init__(__self__, *,
                 configure_mode: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 schedule_expression: Optional[pulumi.Input[str]] = None,
                 schedule_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 targets: Optional[pulumi.Input[str]] = None,
                 template_name: Optional[pulumi.Input[str]] = None,
                 template_version: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering StateConfiguration resources.
        :param pulumi.Input[str] configure_mode: Configuration mode. Valid values: `ApplyAndAutoCorrect`, `ApplyAndMonitor`, `ApplyOnly`.
        :param pulumi.Input[str] description: The description of the resource.
        :param pulumi.Input[str] parameters: The parameter of the Template. This field is in the format of JSON strings. For detailed definition instructions, please refer to [Metadata types that are supported by a configuration list](https://www.alibabacloud.com/help/en/doc-detail/208276.html).
        :param pulumi.Input[str] resource_group_id: The ID of the resource group.
        :param pulumi.Input[str] schedule_expression: Timing expression.
        :param pulumi.Input[str] schedule_type: Timing type. Valid values: `rate`.
        :param pulumi.Input[Mapping[str, Any]] tags: The tag of the resource.
        :param pulumi.Input[str] targets: The Target resources.  This field is in the format of JSON strings. For detailed definition instructions, please refer to [Parameter](https://www.alibabacloud.com/help/en/doc-detail/120674.html).
        :param pulumi.Input[str] template_name: The name of the template.
        :param pulumi.Input[str] template_version: The version number. If you do not specify this parameter, the system uses the latest version.
        """
        if configure_mode is not None:
            pulumi.set(__self__, "configure_mode", configure_mode)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if resource_group_id is not None:
            pulumi.set(__self__, "resource_group_id", resource_group_id)
        if schedule_expression is not None:
            pulumi.set(__self__, "schedule_expression", schedule_expression)
        if schedule_type is not None:
            pulumi.set(__self__, "schedule_type", schedule_type)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if targets is not None:
            pulumi.set(__self__, "targets", targets)
        if template_name is not None:
            pulumi.set(__self__, "template_name", template_name)
        if template_version is not None:
            pulumi.set(__self__, "template_version", template_version)

    @property
    @pulumi.getter(name="configureMode")
    def configure_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Configuration mode. Valid values: `ApplyAndAutoCorrect`, `ApplyAndMonitor`, `ApplyOnly`.
        """
        return pulumi.get(self, "configure_mode")

    @configure_mode.setter
    def configure_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "configure_mode", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[str]]:
        """
        The parameter of the Template. This field is in the format of JSON strings. For detailed definition instructions, please refer to [Metadata types that are supported by a configuration list](https://www.alibabacloud.com/help/en/doc-detail/208276.html).
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the resource group.
        """
        return pulumi.get(self, "resource_group_id")

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_id", value)

    @property
    @pulumi.getter(name="scheduleExpression")
    def schedule_expression(self) -> Optional[pulumi.Input[str]]:
        """
        Timing expression.
        """
        return pulumi.get(self, "schedule_expression")

    @schedule_expression.setter
    def schedule_expression(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schedule_expression", value)

    @property
    @pulumi.getter(name="scheduleType")
    def schedule_type(self) -> Optional[pulumi.Input[str]]:
        """
        Timing type. Valid values: `rate`.
        """
        return pulumi.get(self, "schedule_type")

    @schedule_type.setter
    def schedule_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schedule_type", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        The tag of the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def targets(self) -> Optional[pulumi.Input[str]]:
        """
        The Target resources.  This field is in the format of JSON strings. For detailed definition instructions, please refer to [Parameter](https://www.alibabacloud.com/help/en/doc-detail/120674.html).
        """
        return pulumi.get(self, "targets")

    @targets.setter
    def targets(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "targets", value)

    @property
    @pulumi.getter(name="templateName")
    def template_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the template.
        """
        return pulumi.get(self, "template_name")

    @template_name.setter
    def template_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_name", value)

    @property
    @pulumi.getter(name="templateVersion")
    def template_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version number. If you do not specify this parameter, the system uses the latest version.
        """
        return pulumi.get(self, "template_version")

    @template_version.setter
    def template_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_version", value)


class StateConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configure_mode: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 schedule_expression: Optional[pulumi.Input[str]] = None,
                 schedule_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 targets: Optional[pulumi.Input[str]] = None,
                 template_name: Optional[pulumi.Input[str]] = None,
                 template_version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a OOS State Configuration resource.

        For information about OOS State Configuration and how to use it, see [What is State Configuration](https://www.alibabacloud.com/help/en/doc-detail/208728.html).

        > **NOTE:** Available in v1.147.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default_resource_groups = alicloud.resourcemanager.get_resource_groups()
        default_state_configuration = alicloud.oos.StateConfiguration("defaultStateConfiguration",
            template_name="ACS-ECS-InventoryDataCollection",
            configure_mode="ApplyOnly",
            description=var["name"],
            schedule_type="rate",
            schedule_expression="1 hour",
            resource_group_id=default_resource_groups.ids[0],
            targets="{\\"Filters\\": [{\\"Type\\": \\"All\\", \\"Parameters\\": {\\"InstanceChargeType\\": \\"PrePaid\\"}}], \\"ResourceType\\": \\"ALIYUN::ECS::Instance\\"}",
            parameters="{\\"policy\\": {\\"ACS:Application\\": {\\"Collection\\": \\"Enabled\\"}}}",
            tags={
                "Created": "TF",
                "For": "Test",
            })
        ```

        ## Import

        OOS State Configuration can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:oos/stateConfiguration:StateConfiguration example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] configure_mode: Configuration mode. Valid values: `ApplyAndAutoCorrect`, `ApplyAndMonitor`, `ApplyOnly`.
        :param pulumi.Input[str] description: The description of the resource.
        :param pulumi.Input[str] parameters: The parameter of the Template. This field is in the format of JSON strings. For detailed definition instructions, please refer to [Metadata types that are supported by a configuration list](https://www.alibabacloud.com/help/en/doc-detail/208276.html).
        :param pulumi.Input[str] resource_group_id: The ID of the resource group.
        :param pulumi.Input[str] schedule_expression: Timing expression.
        :param pulumi.Input[str] schedule_type: Timing type. Valid values: `rate`.
        :param pulumi.Input[Mapping[str, Any]] tags: The tag of the resource.
        :param pulumi.Input[str] targets: The Target resources.  This field is in the format of JSON strings. For detailed definition instructions, please refer to [Parameter](https://www.alibabacloud.com/help/en/doc-detail/120674.html).
        :param pulumi.Input[str] template_name: The name of the template.
        :param pulumi.Input[str] template_version: The version number. If you do not specify this parameter, the system uses the latest version.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StateConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a OOS State Configuration resource.

        For information about OOS State Configuration and how to use it, see [What is State Configuration](https://www.alibabacloud.com/help/en/doc-detail/208728.html).

        > **NOTE:** Available in v1.147.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default_resource_groups = alicloud.resourcemanager.get_resource_groups()
        default_state_configuration = alicloud.oos.StateConfiguration("defaultStateConfiguration",
            template_name="ACS-ECS-InventoryDataCollection",
            configure_mode="ApplyOnly",
            description=var["name"],
            schedule_type="rate",
            schedule_expression="1 hour",
            resource_group_id=default_resource_groups.ids[0],
            targets="{\\"Filters\\": [{\\"Type\\": \\"All\\", \\"Parameters\\": {\\"InstanceChargeType\\": \\"PrePaid\\"}}], \\"ResourceType\\": \\"ALIYUN::ECS::Instance\\"}",
            parameters="{\\"policy\\": {\\"ACS:Application\\": {\\"Collection\\": \\"Enabled\\"}}}",
            tags={
                "Created": "TF",
                "For": "Test",
            })
        ```

        ## Import

        OOS State Configuration can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:oos/stateConfiguration:StateConfiguration example <id>
        ```

        :param str resource_name: The name of the resource.
        :param StateConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StateConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configure_mode: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 schedule_expression: Optional[pulumi.Input[str]] = None,
                 schedule_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 targets: Optional[pulumi.Input[str]] = None,
                 template_name: Optional[pulumi.Input[str]] = None,
                 template_version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = StateConfigurationArgs.__new__(StateConfigurationArgs)

            __props__.__dict__["configure_mode"] = configure_mode
            __props__.__dict__["description"] = description
            __props__.__dict__["parameters"] = parameters
            __props__.__dict__["resource_group_id"] = resource_group_id
            if schedule_expression is None and not opts.urn:
                raise TypeError("Missing required property 'schedule_expression'")
            __props__.__dict__["schedule_expression"] = schedule_expression
            if schedule_type is None and not opts.urn:
                raise TypeError("Missing required property 'schedule_type'")
            __props__.__dict__["schedule_type"] = schedule_type
            __props__.__dict__["tags"] = tags
            if targets is None and not opts.urn:
                raise TypeError("Missing required property 'targets'")
            __props__.__dict__["targets"] = targets
            if template_name is None and not opts.urn:
                raise TypeError("Missing required property 'template_name'")
            __props__.__dict__["template_name"] = template_name
            __props__.__dict__["template_version"] = template_version
        super(StateConfiguration, __self__).__init__(
            'alicloud:oos/stateConfiguration:StateConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            configure_mode: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            parameters: Optional[pulumi.Input[str]] = None,
            resource_group_id: Optional[pulumi.Input[str]] = None,
            schedule_expression: Optional[pulumi.Input[str]] = None,
            schedule_type: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            targets: Optional[pulumi.Input[str]] = None,
            template_name: Optional[pulumi.Input[str]] = None,
            template_version: Optional[pulumi.Input[str]] = None) -> 'StateConfiguration':
        """
        Get an existing StateConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] configure_mode: Configuration mode. Valid values: `ApplyAndAutoCorrect`, `ApplyAndMonitor`, `ApplyOnly`.
        :param pulumi.Input[str] description: The description of the resource.
        :param pulumi.Input[str] parameters: The parameter of the Template. This field is in the format of JSON strings. For detailed definition instructions, please refer to [Metadata types that are supported by a configuration list](https://www.alibabacloud.com/help/en/doc-detail/208276.html).
        :param pulumi.Input[str] resource_group_id: The ID of the resource group.
        :param pulumi.Input[str] schedule_expression: Timing expression.
        :param pulumi.Input[str] schedule_type: Timing type. Valid values: `rate`.
        :param pulumi.Input[Mapping[str, Any]] tags: The tag of the resource.
        :param pulumi.Input[str] targets: The Target resources.  This field is in the format of JSON strings. For detailed definition instructions, please refer to [Parameter](https://www.alibabacloud.com/help/en/doc-detail/120674.html).
        :param pulumi.Input[str] template_name: The name of the template.
        :param pulumi.Input[str] template_version: The version number. If you do not specify this parameter, the system uses the latest version.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _StateConfigurationState.__new__(_StateConfigurationState)

        __props__.__dict__["configure_mode"] = configure_mode
        __props__.__dict__["description"] = description
        __props__.__dict__["parameters"] = parameters
        __props__.__dict__["resource_group_id"] = resource_group_id
        __props__.__dict__["schedule_expression"] = schedule_expression
        __props__.__dict__["schedule_type"] = schedule_type
        __props__.__dict__["tags"] = tags
        __props__.__dict__["targets"] = targets
        __props__.__dict__["template_name"] = template_name
        __props__.__dict__["template_version"] = template_version
        return StateConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="configureMode")
    def configure_mode(self) -> pulumi.Output[str]:
        """
        Configuration mode. Valid values: `ApplyAndAutoCorrect`, `ApplyAndMonitor`, `ApplyOnly`.
        """
        return pulumi.get(self, "configure_mode")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Output[Optional[str]]:
        """
        The parameter of the Template. This field is in the format of JSON strings. For detailed definition instructions, please refer to [Metadata types that are supported by a configuration list](https://www.alibabacloud.com/help/en/doc-detail/208276.html).
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> pulumi.Output[str]:
        """
        The ID of the resource group.
        """
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter(name="scheduleExpression")
    def schedule_expression(self) -> pulumi.Output[str]:
        """
        Timing expression.
        """
        return pulumi.get(self, "schedule_expression")

    @property
    @pulumi.getter(name="scheduleType")
    def schedule_type(self) -> pulumi.Output[str]:
        """
        Timing type. Valid values: `rate`.
        """
        return pulumi.get(self, "schedule_type")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        The tag of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def targets(self) -> pulumi.Output[str]:
        """
        The Target resources.  This field is in the format of JSON strings. For detailed definition instructions, please refer to [Parameter](https://www.alibabacloud.com/help/en/doc-detail/120674.html).
        """
        return pulumi.get(self, "targets")

    @property
    @pulumi.getter(name="templateName")
    def template_name(self) -> pulumi.Output[str]:
        """
        The name of the template.
        """
        return pulumi.get(self, "template_name")

    @property
    @pulumi.getter(name="templateVersion")
    def template_version(self) -> pulumi.Output[str]:
        """
        The version number. If you do not specify this parameter, the system uses the latest version.
        """
        return pulumi.get(self, "template_version")

