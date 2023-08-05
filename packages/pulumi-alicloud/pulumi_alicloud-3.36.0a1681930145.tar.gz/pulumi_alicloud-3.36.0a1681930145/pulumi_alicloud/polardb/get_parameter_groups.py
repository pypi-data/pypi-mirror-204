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
    'GetParameterGroupsResult',
    'AwaitableGetParameterGroupsResult',
    'get_parameter_groups',
    'get_parameter_groups_output',
]

@pulumi.output_type
class GetParameterGroupsResult:
    """
    A collection of values returned by getParameterGroups.
    """
    def __init__(__self__, db_type=None, db_version=None, groups=None, id=None, ids=None, name_regex=None, names=None, output_file=None):
        if db_type and not isinstance(db_type, str):
            raise TypeError("Expected argument 'db_type' to be a str")
        pulumi.set(__self__, "db_type", db_type)
        if db_version and not isinstance(db_version, str):
            raise TypeError("Expected argument 'db_version' to be a str")
        pulumi.set(__self__, "db_version", db_version)
        if groups and not isinstance(groups, list):
            raise TypeError("Expected argument 'groups' to be a list")
        pulumi.set(__self__, "groups", groups)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)

    @property
    @pulumi.getter(name="dbType")
    def db_type(self) -> Optional[str]:
        return pulumi.get(self, "db_type")

    @property
    @pulumi.getter(name="dbVersion")
    def db_version(self) -> Optional[str]:
        return pulumi.get(self, "db_version")

    @property
    @pulumi.getter
    def groups(self) -> Sequence['outputs.GetParameterGroupsGroupResult']:
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
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")


class AwaitableGetParameterGroupsResult(GetParameterGroupsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetParameterGroupsResult(
            db_type=self.db_type,
            db_version=self.db_version,
            groups=self.groups,
            id=self.id,
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file)


def get_parameter_groups(db_type: Optional[str] = None,
                         db_version: Optional[str] = None,
                         ids: Optional[Sequence[str]] = None,
                         name_regex: Optional[str] = None,
                         output_file: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetParameterGroupsResult:
    """
    This data source provides the PolarDB Parameter Groups of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.183.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.polardb.get_parameter_groups(ids=["example_id"])
    pulumi.export("polardbParameterGroupId1", ids.groups[0].id)
    name_regex = alicloud.polardb.get_parameter_groups(name_regex="example_name")
    pulumi.export("polardbParameterGroupId2", name_regex.groups[0].id)
    ```


    :param str db_type: The type of the database engine.
    :param str db_version: The version number of the database engine.
    :param Sequence[str] ids: A list of Parameter Group IDs.
    :param str name_regex: A regex string to filter results by Parameter Group name.
    """
    __args__ = dict()
    __args__['dbType'] = db_type
    __args__['dbVersion'] = db_version
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:polardb/getParameterGroups:getParameterGroups', __args__, opts=opts, typ=GetParameterGroupsResult).value

    return AwaitableGetParameterGroupsResult(
        db_type=__ret__.db_type,
        db_version=__ret__.db_version,
        groups=__ret__.groups,
        id=__ret__.id,
        ids=__ret__.ids,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file)


@_utilities.lift_output_func(get_parameter_groups)
def get_parameter_groups_output(db_type: Optional[pulumi.Input[Optional[str]]] = None,
                                db_version: Optional[pulumi.Input[Optional[str]]] = None,
                                ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                                output_file: Optional[pulumi.Input[Optional[str]]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetParameterGroupsResult]:
    """
    This data source provides the PolarDB Parameter Groups of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.183.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.polardb.get_parameter_groups(ids=["example_id"])
    pulumi.export("polardbParameterGroupId1", ids.groups[0].id)
    name_regex = alicloud.polardb.get_parameter_groups(name_regex="example_name")
    pulumi.export("polardbParameterGroupId2", name_regex.groups[0].id)
    ```


    :param str db_type: The type of the database engine.
    :param str db_version: The version number of the database engine.
    :param Sequence[str] ids: A list of Parameter Group IDs.
    :param str name_regex: A regex string to filter results by Parameter Group name.
    """
    ...
