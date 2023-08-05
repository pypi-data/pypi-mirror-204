# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['VbrHaArgs', 'VbrHa']

@pulumi.input_type
class VbrHaArgs:
    def __init__(__self__, *,
                 peer_vbr_id: pulumi.Input[str],
                 vbr_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 vbr_ha_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a VbrHa resource.
        :param pulumi.Input[str] peer_vbr_id: The ID of the other VBR in the VBR failover group.
        :param pulumi.Input[str] vbr_id: The ID of the VBR instance.
        :param pulumi.Input[str] description: The description of the VBR switching group. It must be `2` to `256` characters in length and must start with a letter or Chinese, but cannot start with `https://` or `https://`.
        :param pulumi.Input[bool] dry_run: The dry run.
        :param pulumi.Input[str] vbr_ha_name: The name of the VBR failover group.
        """
        pulumi.set(__self__, "peer_vbr_id", peer_vbr_id)
        pulumi.set(__self__, "vbr_id", vbr_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if dry_run is not None:
            pulumi.set(__self__, "dry_run", dry_run)
        if vbr_ha_name is not None:
            pulumi.set(__self__, "vbr_ha_name", vbr_ha_name)

    @property
    @pulumi.getter(name="peerVbrId")
    def peer_vbr_id(self) -> pulumi.Input[str]:
        """
        The ID of the other VBR in the VBR failover group.
        """
        return pulumi.get(self, "peer_vbr_id")

    @peer_vbr_id.setter
    def peer_vbr_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "peer_vbr_id", value)

    @property
    @pulumi.getter(name="vbrId")
    def vbr_id(self) -> pulumi.Input[str]:
        """
        The ID of the VBR instance.
        """
        return pulumi.get(self, "vbr_id")

    @vbr_id.setter
    def vbr_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vbr_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the VBR switching group. It must be `2` to `256` characters in length and must start with a letter or Chinese, but cannot start with `https://` or `https://`.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="dryRun")
    def dry_run(self) -> Optional[pulumi.Input[bool]]:
        """
        The dry run.
        """
        return pulumi.get(self, "dry_run")

    @dry_run.setter
    def dry_run(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "dry_run", value)

    @property
    @pulumi.getter(name="vbrHaName")
    def vbr_ha_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the VBR failover group.
        """
        return pulumi.get(self, "vbr_ha_name")

    @vbr_ha_name.setter
    def vbr_ha_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vbr_ha_name", value)


@pulumi.input_type
class _VbrHaState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 peer_vbr_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 vbr_ha_name: Optional[pulumi.Input[str]] = None,
                 vbr_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering VbrHa resources.
        :param pulumi.Input[str] description: The description of the VBR switching group. It must be `2` to `256` characters in length and must start with a letter or Chinese, but cannot start with `https://` or `https://`.
        :param pulumi.Input[bool] dry_run: The dry run.
        :param pulumi.Input[str] peer_vbr_id: The ID of the other VBR in the VBR failover group.
        :param pulumi.Input[str] status: The state of the VBR failover group.
        :param pulumi.Input[str] vbr_ha_name: The name of the VBR failover group.
        :param pulumi.Input[str] vbr_id: The ID of the VBR instance.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if dry_run is not None:
            pulumi.set(__self__, "dry_run", dry_run)
        if peer_vbr_id is not None:
            pulumi.set(__self__, "peer_vbr_id", peer_vbr_id)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if vbr_ha_name is not None:
            pulumi.set(__self__, "vbr_ha_name", vbr_ha_name)
        if vbr_id is not None:
            pulumi.set(__self__, "vbr_id", vbr_id)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the VBR switching group. It must be `2` to `256` characters in length and must start with a letter or Chinese, but cannot start with `https://` or `https://`.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="dryRun")
    def dry_run(self) -> Optional[pulumi.Input[bool]]:
        """
        The dry run.
        """
        return pulumi.get(self, "dry_run")

    @dry_run.setter
    def dry_run(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "dry_run", value)

    @property
    @pulumi.getter(name="peerVbrId")
    def peer_vbr_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the other VBR in the VBR failover group.
        """
        return pulumi.get(self, "peer_vbr_id")

    @peer_vbr_id.setter
    def peer_vbr_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "peer_vbr_id", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The state of the VBR failover group.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="vbrHaName")
    def vbr_ha_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the VBR failover group.
        """
        return pulumi.get(self, "vbr_ha_name")

    @vbr_ha_name.setter
    def vbr_ha_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vbr_ha_name", value)

    @property
    @pulumi.getter(name="vbrId")
    def vbr_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the VBR instance.
        """
        return pulumi.get(self, "vbr_id")

    @vbr_id.setter
    def vbr_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vbr_id", value)


class VbrHa(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 peer_vbr_id: Optional[pulumi.Input[str]] = None,
                 vbr_ha_name: Optional[pulumi.Input[str]] = None,
                 vbr_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a VPC Vbr Ha resource.

        For information about VPC Vbr Ha and how to use it, see [What is Vbr Ha](https://www.alibabacloud.com/help/doc-detail/212629.html).

        > **NOTE:** Available in v1.151.0+.

        ## Import

        VPC Vbr Ha can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:vpc/vbrHa:VbrHa example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the VBR switching group. It must be `2` to `256` characters in length and must start with a letter or Chinese, but cannot start with `https://` or `https://`.
        :param pulumi.Input[bool] dry_run: The dry run.
        :param pulumi.Input[str] peer_vbr_id: The ID of the other VBR in the VBR failover group.
        :param pulumi.Input[str] vbr_ha_name: The name of the VBR failover group.
        :param pulumi.Input[str] vbr_id: The ID of the VBR instance.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VbrHaArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a VPC Vbr Ha resource.

        For information about VPC Vbr Ha and how to use it, see [What is Vbr Ha](https://www.alibabacloud.com/help/doc-detail/212629.html).

        > **NOTE:** Available in v1.151.0+.

        ## Import

        VPC Vbr Ha can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:vpc/vbrHa:VbrHa example <id>
        ```

        :param str resource_name: The name of the resource.
        :param VbrHaArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VbrHaArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 peer_vbr_id: Optional[pulumi.Input[str]] = None,
                 vbr_ha_name: Optional[pulumi.Input[str]] = None,
                 vbr_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VbrHaArgs.__new__(VbrHaArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["dry_run"] = dry_run
            if peer_vbr_id is None and not opts.urn:
                raise TypeError("Missing required property 'peer_vbr_id'")
            __props__.__dict__["peer_vbr_id"] = peer_vbr_id
            __props__.__dict__["vbr_ha_name"] = vbr_ha_name
            if vbr_id is None and not opts.urn:
                raise TypeError("Missing required property 'vbr_id'")
            __props__.__dict__["vbr_id"] = vbr_id
            __props__.__dict__["status"] = None
        super(VbrHa, __self__).__init__(
            'alicloud:vpc/vbrHa:VbrHa',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            dry_run: Optional[pulumi.Input[bool]] = None,
            peer_vbr_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            vbr_ha_name: Optional[pulumi.Input[str]] = None,
            vbr_id: Optional[pulumi.Input[str]] = None) -> 'VbrHa':
        """
        Get an existing VbrHa resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the VBR switching group. It must be `2` to `256` characters in length and must start with a letter or Chinese, but cannot start with `https://` or `https://`.
        :param pulumi.Input[bool] dry_run: The dry run.
        :param pulumi.Input[str] peer_vbr_id: The ID of the other VBR in the VBR failover group.
        :param pulumi.Input[str] status: The state of the VBR failover group.
        :param pulumi.Input[str] vbr_ha_name: The name of the VBR failover group.
        :param pulumi.Input[str] vbr_id: The ID of the VBR instance.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VbrHaState.__new__(_VbrHaState)

        __props__.__dict__["description"] = description
        __props__.__dict__["dry_run"] = dry_run
        __props__.__dict__["peer_vbr_id"] = peer_vbr_id
        __props__.__dict__["status"] = status
        __props__.__dict__["vbr_ha_name"] = vbr_ha_name
        __props__.__dict__["vbr_id"] = vbr_id
        return VbrHa(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the VBR switching group. It must be `2` to `256` characters in length and must start with a letter or Chinese, but cannot start with `https://` or `https://`.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="dryRun")
    def dry_run(self) -> pulumi.Output[Optional[bool]]:
        """
        The dry run.
        """
        return pulumi.get(self, "dry_run")

    @property
    @pulumi.getter(name="peerVbrId")
    def peer_vbr_id(self) -> pulumi.Output[str]:
        """
        The ID of the other VBR in the VBR failover group.
        """
        return pulumi.get(self, "peer_vbr_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The state of the VBR failover group.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="vbrHaName")
    def vbr_ha_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the VBR failover group.
        """
        return pulumi.get(self, "vbr_ha_name")

    @property
    @pulumi.getter(name="vbrId")
    def vbr_id(self) -> pulumi.Output[str]:
        """
        The ID of the VBR instance.
        """
        return pulumi.get(self, "vbr_id")

