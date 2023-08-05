# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['PeerConnectionArgs', 'PeerConnection']

@pulumi.input_type
class PeerConnectionArgs:
    def __init__(__self__, *,
                 accepting_ali_uid: pulumi.Input[int],
                 accepting_region_id: pulumi.Input[str],
                 accepting_vpc_id: pulumi.Input[str],
                 vpc_id: pulumi.Input[str],
                 bandwidth: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 peer_connection_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a PeerConnection resource.
        :param pulumi.Input[int] accepting_ali_uid: The ID of the Alibaba Cloud account (primary account) of the receiving end of the VPC peering connection to be created.
               - Enter the ID of your Alibaba Cloud account to create a peer-to-peer connection to the VPC account.
               - Enter the ID of another Alibaba Cloud account to create a cross-account VPC peer-to-peer connection.
               - If the recipient account is a RAM user (sub-account), enter the ID of the Alibaba Cloud account corresponding to the RAM user.
        :param pulumi.Input[str] accepting_region_id: The region ID of the recipient of the VPC peering connection to be created.
               - When creating a VPC peer-to-peer connection in the same region, enter the same region ID as the region ID of the initiator.
               - When creating a cross-region VPC peer-to-peer connection, enter a region ID that is different from the region ID of the initiator.
        :param pulumi.Input[str] accepting_vpc_id: The VPC ID of the receiving end of the VPC peer connection.
        :param pulumi.Input[str] vpc_id: The ID of the requester VPC.
        :param pulumi.Input[int] bandwidth: The bandwidth of the VPC peering connection to be modified. Unit: Mbps. The value range is an integer greater than 0.
        :param pulumi.Input[str] description: The description of the VPC peer connection to be created. It must be 2 to 256 characters in length and must start with a letter or Chinese, but cannot start with `http://` or `https://`.
        :param pulumi.Input[bool] dry_run: The dry run.
        :param pulumi.Input[str] peer_connection_name: The name of the resource. The name must be 2 to 128 characters in length, and must start with a letter. It can contain digits, underscores (_), and hyphens (-).
        :param pulumi.Input[str] status: The status of the resource.
        """
        pulumi.set(__self__, "accepting_ali_uid", accepting_ali_uid)
        pulumi.set(__self__, "accepting_region_id", accepting_region_id)
        pulumi.set(__self__, "accepting_vpc_id", accepting_vpc_id)
        pulumi.set(__self__, "vpc_id", vpc_id)
        if bandwidth is not None:
            pulumi.set(__self__, "bandwidth", bandwidth)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if dry_run is not None:
            pulumi.set(__self__, "dry_run", dry_run)
        if peer_connection_name is not None:
            pulumi.set(__self__, "peer_connection_name", peer_connection_name)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="acceptingAliUid")
    def accepting_ali_uid(self) -> pulumi.Input[int]:
        """
        The ID of the Alibaba Cloud account (primary account) of the receiving end of the VPC peering connection to be created.
        - Enter the ID of your Alibaba Cloud account to create a peer-to-peer connection to the VPC account.
        - Enter the ID of another Alibaba Cloud account to create a cross-account VPC peer-to-peer connection.
        - If the recipient account is a RAM user (sub-account), enter the ID of the Alibaba Cloud account corresponding to the RAM user.
        """
        return pulumi.get(self, "accepting_ali_uid")

    @accepting_ali_uid.setter
    def accepting_ali_uid(self, value: pulumi.Input[int]):
        pulumi.set(self, "accepting_ali_uid", value)

    @property
    @pulumi.getter(name="acceptingRegionId")
    def accepting_region_id(self) -> pulumi.Input[str]:
        """
        The region ID of the recipient of the VPC peering connection to be created.
        - When creating a VPC peer-to-peer connection in the same region, enter the same region ID as the region ID of the initiator.
        - When creating a cross-region VPC peer-to-peer connection, enter a region ID that is different from the region ID of the initiator.
        """
        return pulumi.get(self, "accepting_region_id")

    @accepting_region_id.setter
    def accepting_region_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "accepting_region_id", value)

    @property
    @pulumi.getter(name="acceptingVpcId")
    def accepting_vpc_id(self) -> pulumi.Input[str]:
        """
        The VPC ID of the receiving end of the VPC peer connection.
        """
        return pulumi.get(self, "accepting_vpc_id")

    @accepting_vpc_id.setter
    def accepting_vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "accepting_vpc_id", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Input[str]:
        """
        The ID of the requester VPC.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc_id", value)

    @property
    @pulumi.getter
    def bandwidth(self) -> Optional[pulumi.Input[int]]:
        """
        The bandwidth of the VPC peering connection to be modified. Unit: Mbps. The value range is an integer greater than 0.
        """
        return pulumi.get(self, "bandwidth")

    @bandwidth.setter
    def bandwidth(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "bandwidth", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the VPC peer connection to be created. It must be 2 to 256 characters in length and must start with a letter or Chinese, but cannot start with `http://` or `https://`.
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
    @pulumi.getter(name="peerConnectionName")
    def peer_connection_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource. The name must be 2 to 128 characters in length, and must start with a letter. It can contain digits, underscores (_), and hyphens (-).
        """
        return pulumi.get(self, "peer_connection_name")

    @peer_connection_name.setter
    def peer_connection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "peer_connection_name", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the resource.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class _PeerConnectionState:
    def __init__(__self__, *,
                 accepting_ali_uid: Optional[pulumi.Input[int]] = None,
                 accepting_region_id: Optional[pulumi.Input[str]] = None,
                 accepting_vpc_id: Optional[pulumi.Input[str]] = None,
                 bandwidth: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 peer_connection_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering PeerConnection resources.
        :param pulumi.Input[int] accepting_ali_uid: The ID of the Alibaba Cloud account (primary account) of the receiving end of the VPC peering connection to be created.
               - Enter the ID of your Alibaba Cloud account to create a peer-to-peer connection to the VPC account.
               - Enter the ID of another Alibaba Cloud account to create a cross-account VPC peer-to-peer connection.
               - If the recipient account is a RAM user (sub-account), enter the ID of the Alibaba Cloud account corresponding to the RAM user.
        :param pulumi.Input[str] accepting_region_id: The region ID of the recipient of the VPC peering connection to be created.
               - When creating a VPC peer-to-peer connection in the same region, enter the same region ID as the region ID of the initiator.
               - When creating a cross-region VPC peer-to-peer connection, enter a region ID that is different from the region ID of the initiator.
        :param pulumi.Input[str] accepting_vpc_id: The VPC ID of the receiving end of the VPC peer connection.
        :param pulumi.Input[int] bandwidth: The bandwidth of the VPC peering connection to be modified. Unit: Mbps. The value range is an integer greater than 0.
        :param pulumi.Input[str] description: The description of the VPC peer connection to be created. It must be 2 to 256 characters in length and must start with a letter or Chinese, but cannot start with `http://` or `https://`.
        :param pulumi.Input[bool] dry_run: The dry run.
        :param pulumi.Input[str] peer_connection_name: The name of the resource. The name must be 2 to 128 characters in length, and must start with a letter. It can contain digits, underscores (_), and hyphens (-).
        :param pulumi.Input[str] status: The status of the resource.
        :param pulumi.Input[str] vpc_id: The ID of the requester VPC.
        """
        if accepting_ali_uid is not None:
            pulumi.set(__self__, "accepting_ali_uid", accepting_ali_uid)
        if accepting_region_id is not None:
            pulumi.set(__self__, "accepting_region_id", accepting_region_id)
        if accepting_vpc_id is not None:
            pulumi.set(__self__, "accepting_vpc_id", accepting_vpc_id)
        if bandwidth is not None:
            pulumi.set(__self__, "bandwidth", bandwidth)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if dry_run is not None:
            pulumi.set(__self__, "dry_run", dry_run)
        if peer_connection_name is not None:
            pulumi.set(__self__, "peer_connection_name", peer_connection_name)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="acceptingAliUid")
    def accepting_ali_uid(self) -> Optional[pulumi.Input[int]]:
        """
        The ID of the Alibaba Cloud account (primary account) of the receiving end of the VPC peering connection to be created.
        - Enter the ID of your Alibaba Cloud account to create a peer-to-peer connection to the VPC account.
        - Enter the ID of another Alibaba Cloud account to create a cross-account VPC peer-to-peer connection.
        - If the recipient account is a RAM user (sub-account), enter the ID of the Alibaba Cloud account corresponding to the RAM user.
        """
        return pulumi.get(self, "accepting_ali_uid")

    @accepting_ali_uid.setter
    def accepting_ali_uid(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "accepting_ali_uid", value)

    @property
    @pulumi.getter(name="acceptingRegionId")
    def accepting_region_id(self) -> Optional[pulumi.Input[str]]:
        """
        The region ID of the recipient of the VPC peering connection to be created.
        - When creating a VPC peer-to-peer connection in the same region, enter the same region ID as the region ID of the initiator.
        - When creating a cross-region VPC peer-to-peer connection, enter a region ID that is different from the region ID of the initiator.
        """
        return pulumi.get(self, "accepting_region_id")

    @accepting_region_id.setter
    def accepting_region_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "accepting_region_id", value)

    @property
    @pulumi.getter(name="acceptingVpcId")
    def accepting_vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        The VPC ID of the receiving end of the VPC peer connection.
        """
        return pulumi.get(self, "accepting_vpc_id")

    @accepting_vpc_id.setter
    def accepting_vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "accepting_vpc_id", value)

    @property
    @pulumi.getter
    def bandwidth(self) -> Optional[pulumi.Input[int]]:
        """
        The bandwidth of the VPC peering connection to be modified. Unit: Mbps. The value range is an integer greater than 0.
        """
        return pulumi.get(self, "bandwidth")

    @bandwidth.setter
    def bandwidth(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "bandwidth", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the VPC peer connection to be created. It must be 2 to 256 characters in length and must start with a letter or Chinese, but cannot start with `http://` or `https://`.
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
    @pulumi.getter(name="peerConnectionName")
    def peer_connection_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource. The name must be 2 to 128 characters in length, and must start with a letter. It can contain digits, underscores (_), and hyphens (-).
        """
        return pulumi.get(self, "peer_connection_name")

    @peer_connection_name.setter
    def peer_connection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "peer_connection_name", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the resource.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the requester VPC.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_id", value)


class PeerConnection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 accepting_ali_uid: Optional[pulumi.Input[int]] = None,
                 accepting_region_id: Optional[pulumi.Input[str]] = None,
                 accepting_vpc_id: Optional[pulumi.Input[str]] = None,
                 bandwidth: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 peer_connection_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a VPC Peer Connection resource.

        For information about VPC Peer Connection and how to use it, see [What is Peer Connection](https://www.alibabacloud.com/help/en/virtual-private-cloud/latest/createvpcpeer).

        > **NOTE:** Available in v1.186.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default_account = alicloud.get_account()
        default_networks = alicloud.vpc.get_networks()
        default_peer_connection = alicloud.vpc.PeerConnection("defaultPeerConnection",
            peer_connection_name=var["name"],
            vpc_id=default_networks.ids[0],
            accepting_ali_uid=default_account.id,
            accepting_region_id="cn-hangzhou",
            accepting_vpc_id=default_networks.ids[1],
            description=var["name"])
        ```

        ## Import

        VPC Peer Connection can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:vpc/peerConnection:PeerConnection example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] accepting_ali_uid: The ID of the Alibaba Cloud account (primary account) of the receiving end of the VPC peering connection to be created.
               - Enter the ID of your Alibaba Cloud account to create a peer-to-peer connection to the VPC account.
               - Enter the ID of another Alibaba Cloud account to create a cross-account VPC peer-to-peer connection.
               - If the recipient account is a RAM user (sub-account), enter the ID of the Alibaba Cloud account corresponding to the RAM user.
        :param pulumi.Input[str] accepting_region_id: The region ID of the recipient of the VPC peering connection to be created.
               - When creating a VPC peer-to-peer connection in the same region, enter the same region ID as the region ID of the initiator.
               - When creating a cross-region VPC peer-to-peer connection, enter a region ID that is different from the region ID of the initiator.
        :param pulumi.Input[str] accepting_vpc_id: The VPC ID of the receiving end of the VPC peer connection.
        :param pulumi.Input[int] bandwidth: The bandwidth of the VPC peering connection to be modified. Unit: Mbps. The value range is an integer greater than 0.
        :param pulumi.Input[str] description: The description of the VPC peer connection to be created. It must be 2 to 256 characters in length and must start with a letter or Chinese, but cannot start with `http://` or `https://`.
        :param pulumi.Input[bool] dry_run: The dry run.
        :param pulumi.Input[str] peer_connection_name: The name of the resource. The name must be 2 to 128 characters in length, and must start with a letter. It can contain digits, underscores (_), and hyphens (-).
        :param pulumi.Input[str] status: The status of the resource.
        :param pulumi.Input[str] vpc_id: The ID of the requester VPC.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PeerConnectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a VPC Peer Connection resource.

        For information about VPC Peer Connection and how to use it, see [What is Peer Connection](https://www.alibabacloud.com/help/en/virtual-private-cloud/latest/createvpcpeer).

        > **NOTE:** Available in v1.186.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default_account = alicloud.get_account()
        default_networks = alicloud.vpc.get_networks()
        default_peer_connection = alicloud.vpc.PeerConnection("defaultPeerConnection",
            peer_connection_name=var["name"],
            vpc_id=default_networks.ids[0],
            accepting_ali_uid=default_account.id,
            accepting_region_id="cn-hangzhou",
            accepting_vpc_id=default_networks.ids[1],
            description=var["name"])
        ```

        ## Import

        VPC Peer Connection can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:vpc/peerConnection:PeerConnection example <id>
        ```

        :param str resource_name: The name of the resource.
        :param PeerConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PeerConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 accepting_ali_uid: Optional[pulumi.Input[int]] = None,
                 accepting_region_id: Optional[pulumi.Input[str]] = None,
                 accepting_vpc_id: Optional[pulumi.Input[str]] = None,
                 bandwidth: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 peer_connection_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PeerConnectionArgs.__new__(PeerConnectionArgs)

            if accepting_ali_uid is None and not opts.urn:
                raise TypeError("Missing required property 'accepting_ali_uid'")
            __props__.__dict__["accepting_ali_uid"] = accepting_ali_uid
            if accepting_region_id is None and not opts.urn:
                raise TypeError("Missing required property 'accepting_region_id'")
            __props__.__dict__["accepting_region_id"] = accepting_region_id
            if accepting_vpc_id is None and not opts.urn:
                raise TypeError("Missing required property 'accepting_vpc_id'")
            __props__.__dict__["accepting_vpc_id"] = accepting_vpc_id
            __props__.__dict__["bandwidth"] = bandwidth
            __props__.__dict__["description"] = description
            __props__.__dict__["dry_run"] = dry_run
            __props__.__dict__["peer_connection_name"] = peer_connection_name
            __props__.__dict__["status"] = status
            if vpc_id is None and not opts.urn:
                raise TypeError("Missing required property 'vpc_id'")
            __props__.__dict__["vpc_id"] = vpc_id
        super(PeerConnection, __self__).__init__(
            'alicloud:vpc/peerConnection:PeerConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            accepting_ali_uid: Optional[pulumi.Input[int]] = None,
            accepting_region_id: Optional[pulumi.Input[str]] = None,
            accepting_vpc_id: Optional[pulumi.Input[str]] = None,
            bandwidth: Optional[pulumi.Input[int]] = None,
            description: Optional[pulumi.Input[str]] = None,
            dry_run: Optional[pulumi.Input[bool]] = None,
            peer_connection_name: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            vpc_id: Optional[pulumi.Input[str]] = None) -> 'PeerConnection':
        """
        Get an existing PeerConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] accepting_ali_uid: The ID of the Alibaba Cloud account (primary account) of the receiving end of the VPC peering connection to be created.
               - Enter the ID of your Alibaba Cloud account to create a peer-to-peer connection to the VPC account.
               - Enter the ID of another Alibaba Cloud account to create a cross-account VPC peer-to-peer connection.
               - If the recipient account is a RAM user (sub-account), enter the ID of the Alibaba Cloud account corresponding to the RAM user.
        :param pulumi.Input[str] accepting_region_id: The region ID of the recipient of the VPC peering connection to be created.
               - When creating a VPC peer-to-peer connection in the same region, enter the same region ID as the region ID of the initiator.
               - When creating a cross-region VPC peer-to-peer connection, enter a region ID that is different from the region ID of the initiator.
        :param pulumi.Input[str] accepting_vpc_id: The VPC ID of the receiving end of the VPC peer connection.
        :param pulumi.Input[int] bandwidth: The bandwidth of the VPC peering connection to be modified. Unit: Mbps. The value range is an integer greater than 0.
        :param pulumi.Input[str] description: The description of the VPC peer connection to be created. It must be 2 to 256 characters in length and must start with a letter or Chinese, but cannot start with `http://` or `https://`.
        :param pulumi.Input[bool] dry_run: The dry run.
        :param pulumi.Input[str] peer_connection_name: The name of the resource. The name must be 2 to 128 characters in length, and must start with a letter. It can contain digits, underscores (_), and hyphens (-).
        :param pulumi.Input[str] status: The status of the resource.
        :param pulumi.Input[str] vpc_id: The ID of the requester VPC.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PeerConnectionState.__new__(_PeerConnectionState)

        __props__.__dict__["accepting_ali_uid"] = accepting_ali_uid
        __props__.__dict__["accepting_region_id"] = accepting_region_id
        __props__.__dict__["accepting_vpc_id"] = accepting_vpc_id
        __props__.__dict__["bandwidth"] = bandwidth
        __props__.__dict__["description"] = description
        __props__.__dict__["dry_run"] = dry_run
        __props__.__dict__["peer_connection_name"] = peer_connection_name
        __props__.__dict__["status"] = status
        __props__.__dict__["vpc_id"] = vpc_id
        return PeerConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="acceptingAliUid")
    def accepting_ali_uid(self) -> pulumi.Output[int]:
        """
        The ID of the Alibaba Cloud account (primary account) of the receiving end of the VPC peering connection to be created.
        - Enter the ID of your Alibaba Cloud account to create a peer-to-peer connection to the VPC account.
        - Enter the ID of another Alibaba Cloud account to create a cross-account VPC peer-to-peer connection.
        - If the recipient account is a RAM user (sub-account), enter the ID of the Alibaba Cloud account corresponding to the RAM user.
        """
        return pulumi.get(self, "accepting_ali_uid")

    @property
    @pulumi.getter(name="acceptingRegionId")
    def accepting_region_id(self) -> pulumi.Output[str]:
        """
        The region ID of the recipient of the VPC peering connection to be created.
        - When creating a VPC peer-to-peer connection in the same region, enter the same region ID as the region ID of the initiator.
        - When creating a cross-region VPC peer-to-peer connection, enter a region ID that is different from the region ID of the initiator.
        """
        return pulumi.get(self, "accepting_region_id")

    @property
    @pulumi.getter(name="acceptingVpcId")
    def accepting_vpc_id(self) -> pulumi.Output[str]:
        """
        The VPC ID of the receiving end of the VPC peer connection.
        """
        return pulumi.get(self, "accepting_vpc_id")

    @property
    @pulumi.getter
    def bandwidth(self) -> pulumi.Output[int]:
        """
        The bandwidth of the VPC peering connection to be modified. Unit: Mbps. The value range is an integer greater than 0.
        """
        return pulumi.get(self, "bandwidth")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the VPC peer connection to be created. It must be 2 to 256 characters in length and must start with a letter or Chinese, but cannot start with `http://` or `https://`.
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
    @pulumi.getter(name="peerConnectionName")
    def peer_connection_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the resource. The name must be 2 to 128 characters in length, and must start with a letter. It can contain digits, underscores (_), and hyphens (-).
        """
        return pulumi.get(self, "peer_connection_name")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the resource.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[str]:
        """
        The ID of the requester VPC.
        """
        return pulumi.get(self, "vpc_id")

