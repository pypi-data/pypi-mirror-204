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

__all__ = ['EventRuleArgs', 'EventRule']

@pulumi.input_type
class EventRuleArgs:
    def __init__(__self__, *,
                 event_pattern: pulumi.Input['EventRuleEventPatternArgs'],
                 rule_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 silence_time: Optional[pulumi.Input[int]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a EventRule resource.
        :param pulumi.Input['EventRuleEventPatternArgs'] event_pattern: Event mode, used to describe the trigger conditions for this event. See the following `Block event_pattern`.
        :param pulumi.Input[str] rule_name: The name of the event-triggered alert rule.
        :param pulumi.Input[str] description: The description of the event-triggered alert rule.
        :param pulumi.Input[str] group_id: The ID of the application group to which the event-triggered alert rule belongs.
        :param pulumi.Input[int] silence_time: The silence time.
        :param pulumi.Input[str] status: The status of the resource. Valid values: `ENABLED`, `DISABLED`.
        """
        pulumi.set(__self__, "event_pattern", event_pattern)
        pulumi.set(__self__, "rule_name", rule_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if group_id is not None:
            pulumi.set(__self__, "group_id", group_id)
        if silence_time is not None:
            pulumi.set(__self__, "silence_time", silence_time)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="eventPattern")
    def event_pattern(self) -> pulumi.Input['EventRuleEventPatternArgs']:
        """
        Event mode, used to describe the trigger conditions for this event. See the following `Block event_pattern`.
        """
        return pulumi.get(self, "event_pattern")

    @event_pattern.setter
    def event_pattern(self, value: pulumi.Input['EventRuleEventPatternArgs']):
        pulumi.set(self, "event_pattern", value)

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> pulumi.Input[str]:
        """
        The name of the event-triggered alert rule.
        """
        return pulumi.get(self, "rule_name")

    @rule_name.setter
    def rule_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "rule_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the event-triggered alert rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the application group to which the event-triggered alert rule belongs.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="silenceTime")
    def silence_time(self) -> Optional[pulumi.Input[int]]:
        """
        The silence time.
        """
        return pulumi.get(self, "silence_time")

    @silence_time.setter
    def silence_time(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "silence_time", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the resource. Valid values: `ENABLED`, `DISABLED`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class _EventRuleState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 event_pattern: Optional[pulumi.Input['EventRuleEventPatternArgs']] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 silence_time: Optional[pulumi.Input[int]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering EventRule resources.
        :param pulumi.Input[str] description: The description of the event-triggered alert rule.
        :param pulumi.Input['EventRuleEventPatternArgs'] event_pattern: Event mode, used to describe the trigger conditions for this event. See the following `Block event_pattern`.
        :param pulumi.Input[str] group_id: The ID of the application group to which the event-triggered alert rule belongs.
        :param pulumi.Input[str] rule_name: The name of the event-triggered alert rule.
        :param pulumi.Input[int] silence_time: The silence time.
        :param pulumi.Input[str] status: The status of the resource. Valid values: `ENABLED`, `DISABLED`.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if event_pattern is not None:
            pulumi.set(__self__, "event_pattern", event_pattern)
        if group_id is not None:
            pulumi.set(__self__, "group_id", group_id)
        if rule_name is not None:
            pulumi.set(__self__, "rule_name", rule_name)
        if silence_time is not None:
            pulumi.set(__self__, "silence_time", silence_time)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the event-triggered alert rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="eventPattern")
    def event_pattern(self) -> Optional[pulumi.Input['EventRuleEventPatternArgs']]:
        """
        Event mode, used to describe the trigger conditions for this event. See the following `Block event_pattern`.
        """
        return pulumi.get(self, "event_pattern")

    @event_pattern.setter
    def event_pattern(self, value: Optional[pulumi.Input['EventRuleEventPatternArgs']]):
        pulumi.set(self, "event_pattern", value)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the application group to which the event-triggered alert rule belongs.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the event-triggered alert rule.
        """
        return pulumi.get(self, "rule_name")

    @rule_name.setter
    def rule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rule_name", value)

    @property
    @pulumi.getter(name="silenceTime")
    def silence_time(self) -> Optional[pulumi.Input[int]]:
        """
        The silence time.
        """
        return pulumi.get(self, "silence_time")

    @silence_time.setter
    def silence_time(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "silence_time", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the resource. Valid values: `ENABLED`, `DISABLED`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class EventRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 event_pattern: Optional[pulumi.Input[pulumi.InputType['EventRuleEventPatternArgs']]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 silence_time: Optional[pulumi.Input[int]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Cloud Monitor Service Event Rule resource.

        For information about Cloud Monitor Service Event Rule and how to use it, see [What is Event Rule](https://www.alibabacloud.com/help/en/cloudmonitor/latest/puteventrule).

        > **NOTE:** Available in v1.182.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.cms.MonitorGroup("default", monitor_group_name="example_value")
        example = alicloud.cms.EventRule("example",
            rule_name="example_value",
            group_id=default.id,
            description="example_value",
            status="ENABLED",
            event_pattern=alicloud.cms.EventRuleEventPatternArgs(
                product="ecs",
                event_type_lists=["StatusNotification"],
                level_lists=["CRITICAL"],
                name_lists=["example_value"],
                sql_filter="example_value",
            ),
            silence_time=100)
        ```

        ## Import

        Cloud Monitor Service Event Rule can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cms/eventRule:EventRule example <rule_name>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the event-triggered alert rule.
        :param pulumi.Input[pulumi.InputType['EventRuleEventPatternArgs']] event_pattern: Event mode, used to describe the trigger conditions for this event. See the following `Block event_pattern`.
        :param pulumi.Input[str] group_id: The ID of the application group to which the event-triggered alert rule belongs.
        :param pulumi.Input[str] rule_name: The name of the event-triggered alert rule.
        :param pulumi.Input[int] silence_time: The silence time.
        :param pulumi.Input[str] status: The status of the resource. Valid values: `ENABLED`, `DISABLED`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EventRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Cloud Monitor Service Event Rule resource.

        For information about Cloud Monitor Service Event Rule and how to use it, see [What is Event Rule](https://www.alibabacloud.com/help/en/cloudmonitor/latest/puteventrule).

        > **NOTE:** Available in v1.182.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.cms.MonitorGroup("default", monitor_group_name="example_value")
        example = alicloud.cms.EventRule("example",
            rule_name="example_value",
            group_id=default.id,
            description="example_value",
            status="ENABLED",
            event_pattern=alicloud.cms.EventRuleEventPatternArgs(
                product="ecs",
                event_type_lists=["StatusNotification"],
                level_lists=["CRITICAL"],
                name_lists=["example_value"],
                sql_filter="example_value",
            ),
            silence_time=100)
        ```

        ## Import

        Cloud Monitor Service Event Rule can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cms/eventRule:EventRule example <rule_name>
        ```

        :param str resource_name: The name of the resource.
        :param EventRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EventRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 event_pattern: Optional[pulumi.Input[pulumi.InputType['EventRuleEventPatternArgs']]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 silence_time: Optional[pulumi.Input[int]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EventRuleArgs.__new__(EventRuleArgs)

            __props__.__dict__["description"] = description
            if event_pattern is None and not opts.urn:
                raise TypeError("Missing required property 'event_pattern'")
            __props__.__dict__["event_pattern"] = event_pattern
            __props__.__dict__["group_id"] = group_id
            if rule_name is None and not opts.urn:
                raise TypeError("Missing required property 'rule_name'")
            __props__.__dict__["rule_name"] = rule_name
            __props__.__dict__["silence_time"] = silence_time
            __props__.__dict__["status"] = status
        super(EventRule, __self__).__init__(
            'alicloud:cms/eventRule:EventRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            event_pattern: Optional[pulumi.Input[pulumi.InputType['EventRuleEventPatternArgs']]] = None,
            group_id: Optional[pulumi.Input[str]] = None,
            rule_name: Optional[pulumi.Input[str]] = None,
            silence_time: Optional[pulumi.Input[int]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'EventRule':
        """
        Get an existing EventRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the event-triggered alert rule.
        :param pulumi.Input[pulumi.InputType['EventRuleEventPatternArgs']] event_pattern: Event mode, used to describe the trigger conditions for this event. See the following `Block event_pattern`.
        :param pulumi.Input[str] group_id: The ID of the application group to which the event-triggered alert rule belongs.
        :param pulumi.Input[str] rule_name: The name of the event-triggered alert rule.
        :param pulumi.Input[int] silence_time: The silence time.
        :param pulumi.Input[str] status: The status of the resource. Valid values: `ENABLED`, `DISABLED`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EventRuleState.__new__(_EventRuleState)

        __props__.__dict__["description"] = description
        __props__.__dict__["event_pattern"] = event_pattern
        __props__.__dict__["group_id"] = group_id
        __props__.__dict__["rule_name"] = rule_name
        __props__.__dict__["silence_time"] = silence_time
        __props__.__dict__["status"] = status
        return EventRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the event-triggered alert rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="eventPattern")
    def event_pattern(self) -> pulumi.Output['outputs.EventRuleEventPattern']:
        """
        Event mode, used to describe the trigger conditions for this event. See the following `Block event_pattern`.
        """
        return pulumi.get(self, "event_pattern")

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the application group to which the event-triggered alert rule belongs.
        """
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> pulumi.Output[str]:
        """
        The name of the event-triggered alert rule.
        """
        return pulumi.get(self, "rule_name")

    @property
    @pulumi.getter(name="silenceTime")
    def silence_time(self) -> pulumi.Output[Optional[int]]:
        """
        The silence time.
        """
        return pulumi.get(self, "silence_time")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the resource. Valid values: `ENABLED`, `DISABLED`.
        """
        return pulumi.get(self, "status")

