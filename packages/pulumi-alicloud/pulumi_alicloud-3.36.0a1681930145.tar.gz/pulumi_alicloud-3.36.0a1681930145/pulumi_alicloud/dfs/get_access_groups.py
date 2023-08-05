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
    'GetAccessGroupsResult',
    'AwaitableGetAccessGroupsResult',
    'get_access_groups',
    'get_access_groups_output',
]

@pulumi.output_type
class GetAccessGroupsResult:
    """
    A collection of values returned by getAccessGroups.
    """
    def __init__(__self__, groups=None, id=None, ids=None, limit=None, name_regex=None, names=None, order_by=None, order_type=None, output_file=None, start_offset=None):
        if groups and not isinstance(groups, list):
            raise TypeError("Expected argument 'groups' to be a list")
        pulumi.set(__self__, "groups", groups)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if limit and not isinstance(limit, int):
            raise TypeError("Expected argument 'limit' to be a int")
        pulumi.set(__self__, "limit", limit)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if order_by and not isinstance(order_by, str):
            raise TypeError("Expected argument 'order_by' to be a str")
        pulumi.set(__self__, "order_by", order_by)
        if order_type and not isinstance(order_type, str):
            raise TypeError("Expected argument 'order_type' to be a str")
        pulumi.set(__self__, "order_type", order_type)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if start_offset and not isinstance(start_offset, int):
            raise TypeError("Expected argument 'start_offset' to be a int")
        pulumi.set(__self__, "start_offset", start_offset)

    @property
    @pulumi.getter
    def groups(self) -> Sequence['outputs.GetAccessGroupsGroupResult']:
        return pulumi.get(self, "groups")

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
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter
    def limit(self) -> Optional[int]:
        return pulumi.get(self, "limit")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="orderBy")
    def order_by(self) -> Optional[str]:
        return pulumi.get(self, "order_by")

    @property
    @pulumi.getter(name="orderType")
    def order_type(self) -> Optional[str]:
        return pulumi.get(self, "order_type")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="startOffset")
    def start_offset(self) -> Optional[int]:
        return pulumi.get(self, "start_offset")


class AwaitableGetAccessGroupsResult(GetAccessGroupsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccessGroupsResult(
            groups=self.groups,
            id=self.id,
            ids=self.ids,
            limit=self.limit,
            name_regex=self.name_regex,
            names=self.names,
            order_by=self.order_by,
            order_type=self.order_type,
            output_file=self.output_file,
            start_offset=self.start_offset)


def get_access_groups(ids: Optional[Sequence[str]] = None,
                      limit: Optional[int] = None,
                      name_regex: Optional[str] = None,
                      order_by: Optional[str] = None,
                      order_type: Optional[str] = None,
                      output_file: Optional[str] = None,
                      start_offset: Optional[int] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAccessGroupsResult:
    """
    This data source provides the Apsara File Storage for HDFS Access Groups of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.133.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.dfs.get_access_groups(ids=["example_id"])
    pulumi.export("dfsAccessGroupId1", ids.groups[0].id)
    name_regex = alicloud.dfs.get_access_groups(name_regex="^my-AccessGroup")
    pulumi.export("dfsAccessGroupId2", name_regex.groups[0].id)
    ```


    :param Sequence[str] ids: A list of Access Group IDs.
    :param str name_regex: A regex string to filter results by Access Group name.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['limit'] = limit
    __args__['nameRegex'] = name_regex
    __args__['orderBy'] = order_by
    __args__['orderType'] = order_type
    __args__['outputFile'] = output_file
    __args__['startOffset'] = start_offset
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:dfs/getAccessGroups:getAccessGroups', __args__, opts=opts, typ=GetAccessGroupsResult).value

    return AwaitableGetAccessGroupsResult(
        groups=__ret__.groups,
        id=__ret__.id,
        ids=__ret__.ids,
        limit=__ret__.limit,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        order_by=__ret__.order_by,
        order_type=__ret__.order_type,
        output_file=__ret__.output_file,
        start_offset=__ret__.start_offset)


@_utilities.lift_output_func(get_access_groups)
def get_access_groups_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                             limit: Optional[pulumi.Input[Optional[int]]] = None,
                             name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                             order_by: Optional[pulumi.Input[Optional[str]]] = None,
                             order_type: Optional[pulumi.Input[Optional[str]]] = None,
                             output_file: Optional[pulumi.Input[Optional[str]]] = None,
                             start_offset: Optional[pulumi.Input[Optional[int]]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAccessGroupsResult]:
    """
    This data source provides the Apsara File Storage for HDFS Access Groups of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.133.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.dfs.get_access_groups(ids=["example_id"])
    pulumi.export("dfsAccessGroupId1", ids.groups[0].id)
    name_regex = alicloud.dfs.get_access_groups(name_regex="^my-AccessGroup")
    pulumi.export("dfsAccessGroupId2", name_regex.groups[0].id)
    ```


    :param Sequence[str] ids: A list of Access Group IDs.
    :param str name_regex: A regex string to filter results by Access Group name.
    """
    ...
