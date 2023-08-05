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

__all__ = ['RuleArgs', 'Rule']

@pulumi.input_type
class RuleArgs:
    def __init__(__self__, *,
                 event_bus_name: pulumi.Input[str],
                 filter_pattern: pulumi.Input[str],
                 rule_name: pulumi.Input[str],
                 targets: pulumi.Input[Sequence[pulumi.Input['RuleTargetArgs']]],
                 description: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Rule resource.
        :param pulumi.Input[str] event_bus_name: The name of event bus.
        :param pulumi.Input[str] filter_pattern: The pattern to match interested events. Event mode, JSON format. The value description is as follows: `stringEqual` mode. `stringExpression` mode. Each field has up to 5 expressions (map structure).
        :param pulumi.Input[str] rule_name: The name of rule.
        :param pulumi.Input[Sequence[pulumi.Input['RuleTargetArgs']]] targets: The target of rule.
        :param pulumi.Input[str] description: The description of rule.
        :param pulumi.Input[str] status: Rule status, either Enable or Disable. Valid values: `DISABLE`, `ENABLE`.
        """
        pulumi.set(__self__, "event_bus_name", event_bus_name)
        pulumi.set(__self__, "filter_pattern", filter_pattern)
        pulumi.set(__self__, "rule_name", rule_name)
        pulumi.set(__self__, "targets", targets)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="eventBusName")
    def event_bus_name(self) -> pulumi.Input[str]:
        """
        The name of event bus.
        """
        return pulumi.get(self, "event_bus_name")

    @event_bus_name.setter
    def event_bus_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "event_bus_name", value)

    @property
    @pulumi.getter(name="filterPattern")
    def filter_pattern(self) -> pulumi.Input[str]:
        """
        The pattern to match interested events. Event mode, JSON format. The value description is as follows: `stringEqual` mode. `stringExpression` mode. Each field has up to 5 expressions (map structure).
        """
        return pulumi.get(self, "filter_pattern")

    @filter_pattern.setter
    def filter_pattern(self, value: pulumi.Input[str]):
        pulumi.set(self, "filter_pattern", value)

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> pulumi.Input[str]:
        """
        The name of rule.
        """
        return pulumi.get(self, "rule_name")

    @rule_name.setter
    def rule_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "rule_name", value)

    @property
    @pulumi.getter
    def targets(self) -> pulumi.Input[Sequence[pulumi.Input['RuleTargetArgs']]]:
        """
        The target of rule.
        """
        return pulumi.get(self, "targets")

    @targets.setter
    def targets(self, value: pulumi.Input[Sequence[pulumi.Input['RuleTargetArgs']]]):
        pulumi.set(self, "targets", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Rule status, either Enable or Disable. Valid values: `DISABLE`, `ENABLE`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class _RuleState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 event_bus_name: Optional[pulumi.Input[str]] = None,
                 filter_pattern: Optional[pulumi.Input[str]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 targets: Optional[pulumi.Input[Sequence[pulumi.Input['RuleTargetArgs']]]] = None):
        """
        Input properties used for looking up and filtering Rule resources.
        :param pulumi.Input[str] description: The description of rule.
        :param pulumi.Input[str] event_bus_name: The name of event bus.
        :param pulumi.Input[str] filter_pattern: The pattern to match interested events. Event mode, JSON format. The value description is as follows: `stringEqual` mode. `stringExpression` mode. Each field has up to 5 expressions (map structure).
        :param pulumi.Input[str] rule_name: The name of rule.
        :param pulumi.Input[str] status: Rule status, either Enable or Disable. Valid values: `DISABLE`, `ENABLE`.
        :param pulumi.Input[Sequence[pulumi.Input['RuleTargetArgs']]] targets: The target of rule.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if event_bus_name is not None:
            pulumi.set(__self__, "event_bus_name", event_bus_name)
        if filter_pattern is not None:
            pulumi.set(__self__, "filter_pattern", filter_pattern)
        if rule_name is not None:
            pulumi.set(__self__, "rule_name", rule_name)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if targets is not None:
            pulumi.set(__self__, "targets", targets)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="eventBusName")
    def event_bus_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of event bus.
        """
        return pulumi.get(self, "event_bus_name")

    @event_bus_name.setter
    def event_bus_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "event_bus_name", value)

    @property
    @pulumi.getter(name="filterPattern")
    def filter_pattern(self) -> Optional[pulumi.Input[str]]:
        """
        The pattern to match interested events. Event mode, JSON format. The value description is as follows: `stringEqual` mode. `stringExpression` mode. Each field has up to 5 expressions (map structure).
        """
        return pulumi.get(self, "filter_pattern")

    @filter_pattern.setter
    def filter_pattern(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "filter_pattern", value)

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of rule.
        """
        return pulumi.get(self, "rule_name")

    @rule_name.setter
    def rule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rule_name", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Rule status, either Enable or Disable. Valid values: `DISABLE`, `ENABLE`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def targets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RuleTargetArgs']]]]:
        """
        The target of rule.
        """
        return pulumi.get(self, "targets")

    @targets.setter
    def targets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RuleTargetArgs']]]]):
        pulumi.set(self, "targets", value)


class Rule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 event_bus_name: Optional[pulumi.Input[str]] = None,
                 filter_pattern: Optional[pulumi.Input[str]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 targets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleTargetArgs']]]]] = None,
                 __props__=None):
        """
        Provides a Event Bridge Rule resource.

        For information about Event Bridge Rule and how to use it, see [What is Rule](https://help.aliyun.com/document_detail/167854.html).

        > **NOTE:** Available in v1.129.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example_event_bus = alicloud.eventbridge.EventBus("exampleEventBus", event_bus_name="example_value")
        example_rule = alicloud.eventbridge.Rule("exampleRule",
            event_bus_name=example_event_bus.id,
            rule_name=var["name"],
            description="test",
            filter_pattern="{\\"source\\":[\\"crmabc.newsletter\\"],\\"type\\":[\\"UserSignUp\\", \\"UserLogin\\"]}",
            targets=[alicloud.eventbridge.RuleTargetArgs(
                target_id="tf-test",
                endpoint="acs:mns:cn-hangzhou:118938335****:queues/tf-test",
                type="acs.mns.queue",
                param_lists=[
                    alicloud.eventbridge.RuleTargetParamListArgs(
                        resource_key="queue",
                        form="CONSTANT",
                        value="tf-testaccEbRule",
                    ),
                    alicloud.eventbridge.RuleTargetParamListArgs(
                        resource_key="Body",
                        form="ORIGINAL",
                    ),
                ],
            )])
        ```

        ## Import

        Event Bridge Rule can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:eventbridge/rule:Rule example <event_bus_name>:<rule_name>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of rule.
        :param pulumi.Input[str] event_bus_name: The name of event bus.
        :param pulumi.Input[str] filter_pattern: The pattern to match interested events. Event mode, JSON format. The value description is as follows: `stringEqual` mode. `stringExpression` mode. Each field has up to 5 expressions (map structure).
        :param pulumi.Input[str] rule_name: The name of rule.
        :param pulumi.Input[str] status: Rule status, either Enable or Disable. Valid values: `DISABLE`, `ENABLE`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleTargetArgs']]]] targets: The target of rule.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Event Bridge Rule resource.

        For information about Event Bridge Rule and how to use it, see [What is Rule](https://help.aliyun.com/document_detail/167854.html).

        > **NOTE:** Available in v1.129.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example_event_bus = alicloud.eventbridge.EventBus("exampleEventBus", event_bus_name="example_value")
        example_rule = alicloud.eventbridge.Rule("exampleRule",
            event_bus_name=example_event_bus.id,
            rule_name=var["name"],
            description="test",
            filter_pattern="{\\"source\\":[\\"crmabc.newsletter\\"],\\"type\\":[\\"UserSignUp\\", \\"UserLogin\\"]}",
            targets=[alicloud.eventbridge.RuleTargetArgs(
                target_id="tf-test",
                endpoint="acs:mns:cn-hangzhou:118938335****:queues/tf-test",
                type="acs.mns.queue",
                param_lists=[
                    alicloud.eventbridge.RuleTargetParamListArgs(
                        resource_key="queue",
                        form="CONSTANT",
                        value="tf-testaccEbRule",
                    ),
                    alicloud.eventbridge.RuleTargetParamListArgs(
                        resource_key="Body",
                        form="ORIGINAL",
                    ),
                ],
            )])
        ```

        ## Import

        Event Bridge Rule can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:eventbridge/rule:Rule example <event_bus_name>:<rule_name>
        ```

        :param str resource_name: The name of the resource.
        :param RuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 event_bus_name: Optional[pulumi.Input[str]] = None,
                 filter_pattern: Optional[pulumi.Input[str]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 targets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleTargetArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RuleArgs.__new__(RuleArgs)

            __props__.__dict__["description"] = description
            if event_bus_name is None and not opts.urn:
                raise TypeError("Missing required property 'event_bus_name'")
            __props__.__dict__["event_bus_name"] = event_bus_name
            if filter_pattern is None and not opts.urn:
                raise TypeError("Missing required property 'filter_pattern'")
            __props__.__dict__["filter_pattern"] = filter_pattern
            if rule_name is None and not opts.urn:
                raise TypeError("Missing required property 'rule_name'")
            __props__.__dict__["rule_name"] = rule_name
            __props__.__dict__["status"] = status
            if targets is None and not opts.urn:
                raise TypeError("Missing required property 'targets'")
            __props__.__dict__["targets"] = targets
        super(Rule, __self__).__init__(
            'alicloud:eventbridge/rule:Rule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            event_bus_name: Optional[pulumi.Input[str]] = None,
            filter_pattern: Optional[pulumi.Input[str]] = None,
            rule_name: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            targets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleTargetArgs']]]]] = None) -> 'Rule':
        """
        Get an existing Rule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of rule.
        :param pulumi.Input[str] event_bus_name: The name of event bus.
        :param pulumi.Input[str] filter_pattern: The pattern to match interested events. Event mode, JSON format. The value description is as follows: `stringEqual` mode. `stringExpression` mode. Each field has up to 5 expressions (map structure).
        :param pulumi.Input[str] rule_name: The name of rule.
        :param pulumi.Input[str] status: Rule status, either Enable or Disable. Valid values: `DISABLE`, `ENABLE`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleTargetArgs']]]] targets: The target of rule.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RuleState.__new__(_RuleState)

        __props__.__dict__["description"] = description
        __props__.__dict__["event_bus_name"] = event_bus_name
        __props__.__dict__["filter_pattern"] = filter_pattern
        __props__.__dict__["rule_name"] = rule_name
        __props__.__dict__["status"] = status
        __props__.__dict__["targets"] = targets
        return Rule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="eventBusName")
    def event_bus_name(self) -> pulumi.Output[str]:
        """
        The name of event bus.
        """
        return pulumi.get(self, "event_bus_name")

    @property
    @pulumi.getter(name="filterPattern")
    def filter_pattern(self) -> pulumi.Output[str]:
        """
        The pattern to match interested events. Event mode, JSON format. The value description is as follows: `stringEqual` mode. `stringExpression` mode. Each field has up to 5 expressions (map structure).
        """
        return pulumi.get(self, "filter_pattern")

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> pulumi.Output[str]:
        """
        The name of rule.
        """
        return pulumi.get(self, "rule_name")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Rule status, either Enable or Disable. Valid values: `DISABLE`, `ENABLE`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def targets(self) -> pulumi.Output[Sequence['outputs.RuleTarget']]:
        """
        The target of rule.
        """
        return pulumi.get(self, "targets")

