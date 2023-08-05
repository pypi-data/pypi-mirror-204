# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['BandwidthPackageAttachmentArgs', 'BandwidthPackageAttachment']

@pulumi.input_type
class BandwidthPackageAttachmentArgs:
    def __init__(__self__, *,
                 accelerator_id: pulumi.Input[str],
                 bandwidth_package_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a BandwidthPackageAttachment resource.
        :param pulumi.Input[str] accelerator_id: The ID of the Global Accelerator instance from which you want to disassociate the bandwidth plan.
        :param pulumi.Input[str] bandwidth_package_id: The ID of the bandwidth plan to disassociate. **NOTE:** From version 1.192.0, `bandwidth_package_id` can be modified.
        """
        pulumi.set(__self__, "accelerator_id", accelerator_id)
        pulumi.set(__self__, "bandwidth_package_id", bandwidth_package_id)

    @property
    @pulumi.getter(name="acceleratorId")
    def accelerator_id(self) -> pulumi.Input[str]:
        """
        The ID of the Global Accelerator instance from which you want to disassociate the bandwidth plan.
        """
        return pulumi.get(self, "accelerator_id")

    @accelerator_id.setter
    def accelerator_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "accelerator_id", value)

    @property
    @pulumi.getter(name="bandwidthPackageId")
    def bandwidth_package_id(self) -> pulumi.Input[str]:
        """
        The ID of the bandwidth plan to disassociate. **NOTE:** From version 1.192.0, `bandwidth_package_id` can be modified.
        """
        return pulumi.get(self, "bandwidth_package_id")

    @bandwidth_package_id.setter
    def bandwidth_package_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "bandwidth_package_id", value)


@pulumi.input_type
class _BandwidthPackageAttachmentState:
    def __init__(__self__, *,
                 accelerator_id: Optional[pulumi.Input[str]] = None,
                 accelerators: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 bandwidth_package_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BandwidthPackageAttachment resources.
        :param pulumi.Input[str] accelerator_id: The ID of the Global Accelerator instance from which you want to disassociate the bandwidth plan.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] accelerators: Accelerators bound with current Bandwidth Package.
        :param pulumi.Input[str] bandwidth_package_id: The ID of the bandwidth plan to disassociate. **NOTE:** From version 1.192.0, `bandwidth_package_id` can be modified.
        :param pulumi.Input[str] status: State of Bandwidth Package.
        """
        if accelerator_id is not None:
            pulumi.set(__self__, "accelerator_id", accelerator_id)
        if accelerators is not None:
            pulumi.set(__self__, "accelerators", accelerators)
        if bandwidth_package_id is not None:
            pulumi.set(__self__, "bandwidth_package_id", bandwidth_package_id)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="acceleratorId")
    def accelerator_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Global Accelerator instance from which you want to disassociate the bandwidth plan.
        """
        return pulumi.get(self, "accelerator_id")

    @accelerator_id.setter
    def accelerator_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "accelerator_id", value)

    @property
    @pulumi.getter
    def accelerators(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Accelerators bound with current Bandwidth Package.
        """
        return pulumi.get(self, "accelerators")

    @accelerators.setter
    def accelerators(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "accelerators", value)

    @property
    @pulumi.getter(name="bandwidthPackageId")
    def bandwidth_package_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the bandwidth plan to disassociate. **NOTE:** From version 1.192.0, `bandwidth_package_id` can be modified.
        """
        return pulumi.get(self, "bandwidth_package_id")

    @bandwidth_package_id.setter
    def bandwidth_package_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bandwidth_package_id", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        State of Bandwidth Package.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class BandwidthPackageAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 accelerator_id: Optional[pulumi.Input[str]] = None,
                 bandwidth_package_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Global Accelerator (GA) Bandwidth Package Attachment resource.

        For information about Global Accelerator (GA) Bandwidth Package Attachment and how to use it, see [What is Bandwidth Package Attachment](https://www.alibabacloud.com/help/en/global-accelerator/latest/bandwidthpackageaddaccelerator).

        > **NOTE:** Available in v1.113.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example_accelerator = alicloud.ga.Accelerator("exampleAccelerator",
            duration=1,
            auto_use_coupon=True,
            spec="1")
        example_bandwidth_package = alicloud.ga.BandwidthPackage("exampleBandwidthPackage",
            bandwidth=20,
            type="Basic",
            bandwidth_type="Basic",
            duration="1",
            auto_pay=True,
            ratio=30)
        example_bandwidth_package_attachment = alicloud.ga.BandwidthPackageAttachment("exampleBandwidthPackageAttachment",
            accelerator_id=example_accelerator.id,
            bandwidth_package_id=example_bandwidth_package.id)
        ```

        ## Import

        Ga Bandwidth Package Attachment can be imported using the id. Format to `<accelerator_id>:<bandwidth_package_id>`, e.g.

        ```sh
         $ pulumi import alicloud:ga/bandwidthPackageAttachment:BandwidthPackageAttachment example your_accelerator_id:your_bandwidth_package_id
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accelerator_id: The ID of the Global Accelerator instance from which you want to disassociate the bandwidth plan.
        :param pulumi.Input[str] bandwidth_package_id: The ID of the bandwidth plan to disassociate. **NOTE:** From version 1.192.0, `bandwidth_package_id` can be modified.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BandwidthPackageAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Global Accelerator (GA) Bandwidth Package Attachment resource.

        For information about Global Accelerator (GA) Bandwidth Package Attachment and how to use it, see [What is Bandwidth Package Attachment](https://www.alibabacloud.com/help/en/global-accelerator/latest/bandwidthpackageaddaccelerator).

        > **NOTE:** Available in v1.113.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example_accelerator = alicloud.ga.Accelerator("exampleAccelerator",
            duration=1,
            auto_use_coupon=True,
            spec="1")
        example_bandwidth_package = alicloud.ga.BandwidthPackage("exampleBandwidthPackage",
            bandwidth=20,
            type="Basic",
            bandwidth_type="Basic",
            duration="1",
            auto_pay=True,
            ratio=30)
        example_bandwidth_package_attachment = alicloud.ga.BandwidthPackageAttachment("exampleBandwidthPackageAttachment",
            accelerator_id=example_accelerator.id,
            bandwidth_package_id=example_bandwidth_package.id)
        ```

        ## Import

        Ga Bandwidth Package Attachment can be imported using the id. Format to `<accelerator_id>:<bandwidth_package_id>`, e.g.

        ```sh
         $ pulumi import alicloud:ga/bandwidthPackageAttachment:BandwidthPackageAttachment example your_accelerator_id:your_bandwidth_package_id
        ```

        :param str resource_name: The name of the resource.
        :param BandwidthPackageAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BandwidthPackageAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 accelerator_id: Optional[pulumi.Input[str]] = None,
                 bandwidth_package_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BandwidthPackageAttachmentArgs.__new__(BandwidthPackageAttachmentArgs)

            if accelerator_id is None and not opts.urn:
                raise TypeError("Missing required property 'accelerator_id'")
            __props__.__dict__["accelerator_id"] = accelerator_id
            if bandwidth_package_id is None and not opts.urn:
                raise TypeError("Missing required property 'bandwidth_package_id'")
            __props__.__dict__["bandwidth_package_id"] = bandwidth_package_id
            __props__.__dict__["accelerators"] = None
            __props__.__dict__["status"] = None
        super(BandwidthPackageAttachment, __self__).__init__(
            'alicloud:ga/bandwidthPackageAttachment:BandwidthPackageAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            accelerator_id: Optional[pulumi.Input[str]] = None,
            accelerators: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            bandwidth_package_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'BandwidthPackageAttachment':
        """
        Get an existing BandwidthPackageAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accelerator_id: The ID of the Global Accelerator instance from which you want to disassociate the bandwidth plan.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] accelerators: Accelerators bound with current Bandwidth Package.
        :param pulumi.Input[str] bandwidth_package_id: The ID of the bandwidth plan to disassociate. **NOTE:** From version 1.192.0, `bandwidth_package_id` can be modified.
        :param pulumi.Input[str] status: State of Bandwidth Package.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BandwidthPackageAttachmentState.__new__(_BandwidthPackageAttachmentState)

        __props__.__dict__["accelerator_id"] = accelerator_id
        __props__.__dict__["accelerators"] = accelerators
        __props__.__dict__["bandwidth_package_id"] = bandwidth_package_id
        __props__.__dict__["status"] = status
        return BandwidthPackageAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="acceleratorId")
    def accelerator_id(self) -> pulumi.Output[str]:
        """
        The ID of the Global Accelerator instance from which you want to disassociate the bandwidth plan.
        """
        return pulumi.get(self, "accelerator_id")

    @property
    @pulumi.getter
    def accelerators(self) -> pulumi.Output[Sequence[str]]:
        """
        Accelerators bound with current Bandwidth Package.
        """
        return pulumi.get(self, "accelerators")

    @property
    @pulumi.getter(name="bandwidthPackageId")
    def bandwidth_package_id(self) -> pulumi.Output[str]:
        """
        The ID of the bandwidth plan to disassociate. **NOTE:** From version 1.192.0, `bandwidth_package_id` can be modified.
        """
        return pulumi.get(self, "bandwidth_package_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        State of Bandwidth Package.
        """
        return pulumi.get(self, "status")

