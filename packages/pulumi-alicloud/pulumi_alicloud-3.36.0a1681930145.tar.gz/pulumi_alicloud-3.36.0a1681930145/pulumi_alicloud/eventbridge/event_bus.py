# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['EventBusArgs', 'EventBus']

@pulumi.input_type
class EventBusArgs:
    def __init__(__self__, *,
                 event_bus_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a EventBus resource.
        :param pulumi.Input[str] event_bus_name: The name of event bus. The length is limited to 2 ~ 127 characters, which can be composed of letters, numbers or hyphens (-)
        :param pulumi.Input[str] description: The description of event bus.
        """
        pulumi.set(__self__, "event_bus_name", event_bus_name)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter(name="eventBusName")
    def event_bus_name(self) -> pulumi.Input[str]:
        """
        The name of event bus. The length is limited to 2 ~ 127 characters, which can be composed of letters, numbers or hyphens (-)
        """
        return pulumi.get(self, "event_bus_name")

    @event_bus_name.setter
    def event_bus_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "event_bus_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of event bus.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class _EventBusState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 event_bus_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering EventBus resources.
        :param pulumi.Input[str] description: The description of event bus.
        :param pulumi.Input[str] event_bus_name: The name of event bus. The length is limited to 2 ~ 127 characters, which can be composed of letters, numbers or hyphens (-)
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if event_bus_name is not None:
            pulumi.set(__self__, "event_bus_name", event_bus_name)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of event bus.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="eventBusName")
    def event_bus_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of event bus. The length is limited to 2 ~ 127 characters, which can be composed of letters, numbers or hyphens (-)
        """
        return pulumi.get(self, "event_bus_name")

    @event_bus_name.setter
    def event_bus_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "event_bus_name", value)


class EventBus(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 event_bus_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Event Bridge Event Bus resource.

        For information about Event Bridge Event Bus and how to use it, see [What is Event Bus](https://help.aliyun.com/document_detail/167863.html).

        > **NOTE:** Available in v1.129.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example = alicloud.eventbridge.EventBus("example", event_bus_name="my-EventBus")
        ```

        ## Import

        Event Bridge Event Bus can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:eventbridge/eventBus:EventBus example <event_bus_name>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of event bus.
        :param pulumi.Input[str] event_bus_name: The name of event bus. The length is limited to 2 ~ 127 characters, which can be composed of letters, numbers or hyphens (-)
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EventBusArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Event Bridge Event Bus resource.

        For information about Event Bridge Event Bus and how to use it, see [What is Event Bus](https://help.aliyun.com/document_detail/167863.html).

        > **NOTE:** Available in v1.129.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example = alicloud.eventbridge.EventBus("example", event_bus_name="my-EventBus")
        ```

        ## Import

        Event Bridge Event Bus can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:eventbridge/eventBus:EventBus example <event_bus_name>
        ```

        :param str resource_name: The name of the resource.
        :param EventBusArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EventBusArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 event_bus_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EventBusArgs.__new__(EventBusArgs)

            __props__.__dict__["description"] = description
            if event_bus_name is None and not opts.urn:
                raise TypeError("Missing required property 'event_bus_name'")
            __props__.__dict__["event_bus_name"] = event_bus_name
        super(EventBus, __self__).__init__(
            'alicloud:eventbridge/eventBus:EventBus',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            event_bus_name: Optional[pulumi.Input[str]] = None) -> 'EventBus':
        """
        Get an existing EventBus resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of event bus.
        :param pulumi.Input[str] event_bus_name: The name of event bus. The length is limited to 2 ~ 127 characters, which can be composed of letters, numbers or hyphens (-)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EventBusState.__new__(_EventBusState)

        __props__.__dict__["description"] = description
        __props__.__dict__["event_bus_name"] = event_bus_name
        return EventBus(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of event bus.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="eventBusName")
    def event_bus_name(self) -> pulumi.Output[str]:
        """
        The name of event bus. The length is limited to 2 ~ 127 characters, which can be composed of letters, numbers or hyphens (-)
        """
        return pulumi.get(self, "event_bus_name")

