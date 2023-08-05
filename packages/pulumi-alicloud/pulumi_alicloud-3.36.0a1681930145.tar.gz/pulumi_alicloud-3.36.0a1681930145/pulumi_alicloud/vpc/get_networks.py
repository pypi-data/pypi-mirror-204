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

__all__ = [
    'GetNetworksResult',
    'AwaitableGetNetworksResult',
    'get_networks',
    'get_networks_output',
]

@pulumi.output_type
class GetNetworksResult:
    """
    A collection of values returned by getNetworks.
    """
    def __init__(__self__, cidr_block=None, dhcp_options_set_id=None, dry_run=None, enable_details=None, id=None, ids=None, is_default=None, name_regex=None, names=None, output_file=None, page_number=None, page_size=None, resource_group_id=None, status=None, tags=None, total_count=None, vpc_name=None, vpc_owner_id=None, vpcs=None, vswitch_id=None):
        if cidr_block and not isinstance(cidr_block, str):
            raise TypeError("Expected argument 'cidr_block' to be a str")
        pulumi.set(__self__, "cidr_block", cidr_block)
        if dhcp_options_set_id and not isinstance(dhcp_options_set_id, str):
            raise TypeError("Expected argument 'dhcp_options_set_id' to be a str")
        pulumi.set(__self__, "dhcp_options_set_id", dhcp_options_set_id)
        if dry_run and not isinstance(dry_run, bool):
            raise TypeError("Expected argument 'dry_run' to be a bool")
        pulumi.set(__self__, "dry_run", dry_run)
        if enable_details and not isinstance(enable_details, bool):
            raise TypeError("Expected argument 'enable_details' to be a bool")
        pulumi.set(__self__, "enable_details", enable_details)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if is_default and not isinstance(is_default, bool):
            raise TypeError("Expected argument 'is_default' to be a bool")
        pulumi.set(__self__, "is_default", is_default)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if page_number and not isinstance(page_number, int):
            raise TypeError("Expected argument 'page_number' to be a int")
        pulumi.set(__self__, "page_number", page_number)
        if page_size and not isinstance(page_size, int):
            raise TypeError("Expected argument 'page_size' to be a int")
        pulumi.set(__self__, "page_size", page_size)
        if resource_group_id and not isinstance(resource_group_id, str):
            raise TypeError("Expected argument 'resource_group_id' to be a str")
        pulumi.set(__self__, "resource_group_id", resource_group_id)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if total_count and not isinstance(total_count, int):
            raise TypeError("Expected argument 'total_count' to be a int")
        pulumi.set(__self__, "total_count", total_count)
        if vpc_name and not isinstance(vpc_name, str):
            raise TypeError("Expected argument 'vpc_name' to be a str")
        pulumi.set(__self__, "vpc_name", vpc_name)
        if vpc_owner_id and not isinstance(vpc_owner_id, int):
            raise TypeError("Expected argument 'vpc_owner_id' to be a int")
        pulumi.set(__self__, "vpc_owner_id", vpc_owner_id)
        if vpcs and not isinstance(vpcs, list):
            raise TypeError("Expected argument 'vpcs' to be a list")
        pulumi.set(__self__, "vpcs", vpcs)
        if vswitch_id and not isinstance(vswitch_id, str):
            raise TypeError("Expected argument 'vswitch_id' to be a str")
        pulumi.set(__self__, "vswitch_id", vswitch_id)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> Optional[str]:
        """
        CIDR block of the VPC.
        """
        return pulumi.get(self, "cidr_block")

    @property
    @pulumi.getter(name="dhcpOptionsSetId")
    def dhcp_options_set_id(self) -> Optional[str]:
        return pulumi.get(self, "dhcp_options_set_id")

    @property
    @pulumi.getter(name="dryRun")
    def dry_run(self) -> Optional[bool]:
        return pulumi.get(self, "dry_run")

    @property
    @pulumi.getter(name="enableDetails")
    def enable_details(self) -> Optional[bool]:
        return pulumi.get(self, "enable_details")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        """
        A list of VPC IDs.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="isDefault")
    def is_default(self) -> Optional[bool]:
        """
        Whether the VPC is the default VPC in the region.
        """
        return pulumi.get(self, "is_default")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        """
        A list of VPC names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="pageNumber")
    def page_number(self) -> Optional[int]:
        return pulumi.get(self, "page_number")

    @property
    @pulumi.getter(name="pageSize")
    def page_size(self) -> Optional[int]:
        return pulumi.get(self, "page_size")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[str]:
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        Status of the VPC.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, Any]]:
        """
        A map of tags assigned to the VPC.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="totalCount")
    def total_count(self) -> int:
        return pulumi.get(self, "total_count")

    @property
    @pulumi.getter(name="vpcName")
    def vpc_name(self) -> Optional[str]:
        """
        Name of the VPC.
        """
        return pulumi.get(self, "vpc_name")

    @property
    @pulumi.getter(name="vpcOwnerId")
    def vpc_owner_id(self) -> Optional[int]:
        return pulumi.get(self, "vpc_owner_id")

    @property
    @pulumi.getter
    def vpcs(self) -> Sequence['outputs.GetNetworksVpcResult']:
        """
        A list of VPCs. Each element contains the following attributes:
        """
        return pulumi.get(self, "vpcs")

    @property
    @pulumi.getter(name="vswitchId")
    def vswitch_id(self) -> Optional[str]:
        return pulumi.get(self, "vswitch_id")


class AwaitableGetNetworksResult(GetNetworksResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNetworksResult(
            cidr_block=self.cidr_block,
            dhcp_options_set_id=self.dhcp_options_set_id,
            dry_run=self.dry_run,
            enable_details=self.enable_details,
            id=self.id,
            ids=self.ids,
            is_default=self.is_default,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            page_number=self.page_number,
            page_size=self.page_size,
            resource_group_id=self.resource_group_id,
            status=self.status,
            tags=self.tags,
            total_count=self.total_count,
            vpc_name=self.vpc_name,
            vpc_owner_id=self.vpc_owner_id,
            vpcs=self.vpcs,
            vswitch_id=self.vswitch_id)


def get_networks(cidr_block: Optional[str] = None,
                 dhcp_options_set_id: Optional[str] = None,
                 dry_run: Optional[bool] = None,
                 enable_details: Optional[bool] = None,
                 ids: Optional[Sequence[str]] = None,
                 is_default: Optional[bool] = None,
                 name_regex: Optional[str] = None,
                 output_file: Optional[str] = None,
                 page_number: Optional[int] = None,
                 page_size: Optional[int] = None,
                 resource_group_id: Optional[str] = None,
                 status: Optional[str] = None,
                 tags: Optional[Mapping[str, Any]] = None,
                 vpc_name: Optional[str] = None,
                 vpc_owner_id: Optional[int] = None,
                 vswitch_id: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNetworksResult:
    """
    This data source provides VPCs available to the user.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    vpcs_ds = alicloud.vpc.get_networks(cidr_block="172.16.0.0/12",
        name_regex="^foo",
        status="Available")
    pulumi.export("firstVpcId", vpcs_ds.vpcs[0].id)
    ```


    :param str cidr_block: Filter results by a specific CIDR block. For example: "172.16.0.0/12".
    :param str dhcp_options_set_id: The ID of dhcp options set.
    :param bool dry_run: Indicates whether to check this request only. Valid values: `true` and `false`.
    :param bool enable_details: Default to `true`. Set it to true can output the `route_table_id`.
    :param Sequence[str] ids: A list of VPC IDs.
    :param bool is_default: Indicate whether the VPC is the default one in the specified region.
    :param str name_regex: A regex string to filter VPCs by name.
    :param str resource_group_id: The Id of resource group which VPC belongs.
    :param str status: Filter results by a specific status. Valid value are `Pending` and `Available`.
    :param Mapping[str, Any] tags: A mapping of tags to assign to the resource.
    :param str vpc_name: The name of the VPC.
    :param int vpc_owner_id: The owner ID of VPC.
    :param str vswitch_id: Filter results by the specified VSwitch.
    """
    __args__ = dict()
    __args__['cidrBlock'] = cidr_block
    __args__['dhcpOptionsSetId'] = dhcp_options_set_id
    __args__['dryRun'] = dry_run
    __args__['enableDetails'] = enable_details
    __args__['ids'] = ids
    __args__['isDefault'] = is_default
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['pageNumber'] = page_number
    __args__['pageSize'] = page_size
    __args__['resourceGroupId'] = resource_group_id
    __args__['status'] = status
    __args__['tags'] = tags
    __args__['vpcName'] = vpc_name
    __args__['vpcOwnerId'] = vpc_owner_id
    __args__['vswitchId'] = vswitch_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:vpc/getNetworks:getNetworks', __args__, opts=opts, typ=GetNetworksResult).value

    return AwaitableGetNetworksResult(
        cidr_block=__ret__.cidr_block,
        dhcp_options_set_id=__ret__.dhcp_options_set_id,
        dry_run=__ret__.dry_run,
        enable_details=__ret__.enable_details,
        id=__ret__.id,
        ids=__ret__.ids,
        is_default=__ret__.is_default,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file,
        page_number=__ret__.page_number,
        page_size=__ret__.page_size,
        resource_group_id=__ret__.resource_group_id,
        status=__ret__.status,
        tags=__ret__.tags,
        total_count=__ret__.total_count,
        vpc_name=__ret__.vpc_name,
        vpc_owner_id=__ret__.vpc_owner_id,
        vpcs=__ret__.vpcs,
        vswitch_id=__ret__.vswitch_id)


@_utilities.lift_output_func(get_networks)
def get_networks_output(cidr_block: Optional[pulumi.Input[Optional[str]]] = None,
                        dhcp_options_set_id: Optional[pulumi.Input[Optional[str]]] = None,
                        dry_run: Optional[pulumi.Input[Optional[bool]]] = None,
                        enable_details: Optional[pulumi.Input[Optional[bool]]] = None,
                        ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                        is_default: Optional[pulumi.Input[Optional[bool]]] = None,
                        name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                        output_file: Optional[pulumi.Input[Optional[str]]] = None,
                        page_number: Optional[pulumi.Input[Optional[int]]] = None,
                        page_size: Optional[pulumi.Input[Optional[int]]] = None,
                        resource_group_id: Optional[pulumi.Input[Optional[str]]] = None,
                        status: Optional[pulumi.Input[Optional[str]]] = None,
                        tags: Optional[pulumi.Input[Optional[Mapping[str, Any]]]] = None,
                        vpc_name: Optional[pulumi.Input[Optional[str]]] = None,
                        vpc_owner_id: Optional[pulumi.Input[Optional[int]]] = None,
                        vswitch_id: Optional[pulumi.Input[Optional[str]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNetworksResult]:
    """
    This data source provides VPCs available to the user.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    vpcs_ds = alicloud.vpc.get_networks(cidr_block="172.16.0.0/12",
        name_regex="^foo",
        status="Available")
    pulumi.export("firstVpcId", vpcs_ds.vpcs[0].id)
    ```


    :param str cidr_block: Filter results by a specific CIDR block. For example: "172.16.0.0/12".
    :param str dhcp_options_set_id: The ID of dhcp options set.
    :param bool dry_run: Indicates whether to check this request only. Valid values: `true` and `false`.
    :param bool enable_details: Default to `true`. Set it to true can output the `route_table_id`.
    :param Sequence[str] ids: A list of VPC IDs.
    :param bool is_default: Indicate whether the VPC is the default one in the specified region.
    :param str name_regex: A regex string to filter VPCs by name.
    :param str resource_group_id: The Id of resource group which VPC belongs.
    :param str status: Filter results by a specific status. Valid value are `Pending` and `Available`.
    :param Mapping[str, Any] tags: A mapping of tags to assign to the resource.
    :param str vpc_name: The name of the VPC.
    :param int vpc_owner_id: The owner ID of VPC.
    :param str vswitch_id: Filter results by the specified VSwitch.
    """
    ...
