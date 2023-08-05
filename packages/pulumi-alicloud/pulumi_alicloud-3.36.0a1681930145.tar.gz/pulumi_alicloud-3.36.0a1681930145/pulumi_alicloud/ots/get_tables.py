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
    'GetTablesResult',
    'AwaitableGetTablesResult',
    'get_tables',
    'get_tables_output',
]

@pulumi.output_type
class GetTablesResult:
    """
    A collection of values returned by getTables.
    """
    def __init__(__self__, id=None, ids=None, instance_name=None, name_regex=None, names=None, output_file=None, tables=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if instance_name and not isinstance(instance_name, str):
            raise TypeError("Expected argument 'instance_name' to be a str")
        pulumi.set(__self__, "instance_name", instance_name)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if tables and not isinstance(tables, list):
            raise TypeError("Expected argument 'tables' to be a list")
        pulumi.set(__self__, "tables", tables)

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
        A list of table IDs.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="instanceName")
    def instance_name(self) -> str:
        """
        The OTS instance name.
        """
        return pulumi.get(self, "instance_name")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        """
        A list of table names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def tables(self) -> Sequence['outputs.GetTablesTableResult']:
        """
        A list of tables. Each element contains the following attributes:
        """
        return pulumi.get(self, "tables")


class AwaitableGetTablesResult(GetTablesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTablesResult(
            id=self.id,
            ids=self.ids,
            instance_name=self.instance_name,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            tables=self.tables)


def get_tables(ids: Optional[Sequence[str]] = None,
               instance_name: Optional[str] = None,
               name_regex: Optional[str] = None,
               output_file: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTablesResult:
    """
    This data source provides the ots tables of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.40.0+.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    tables_ds = alicloud.ots.get_tables(instance_name="sample-instance",
        name_regex="sample-table",
        output_file="tables.txt")
    pulumi.export("firstTableId", tables_ds.tables[0].id)
    ```


    :param Sequence[str] ids: A list of table IDs.
    :param str instance_name: The name of OTS instance.
    :param str name_regex: A regex string to filter results by table name.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['instanceName'] = instance_name
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:ots/getTables:getTables', __args__, opts=opts, typ=GetTablesResult).value

    return AwaitableGetTablesResult(
        id=__ret__.id,
        ids=__ret__.ids,
        instance_name=__ret__.instance_name,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file,
        tables=__ret__.tables)


@_utilities.lift_output_func(get_tables)
def get_tables_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                      instance_name: Optional[pulumi.Input[str]] = None,
                      name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                      output_file: Optional[pulumi.Input[Optional[str]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTablesResult]:
    """
    This data source provides the ots tables of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.40.0+.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    tables_ds = alicloud.ots.get_tables(instance_name="sample-instance",
        name_regex="sample-table",
        output_file="tables.txt")
    pulumi.export("firstTableId", tables_ds.tables[0].id)
    ```


    :param Sequence[str] ids: A list of table IDs.
    :param str instance_name: The name of OTS instance.
    :param str name_regex: A regex string to filter results by table name.
    """
    ...
