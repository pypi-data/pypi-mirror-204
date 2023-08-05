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
    'GetFoldersResult',
    'AwaitableGetFoldersResult',
    'get_folders',
    'get_folders_output',
]

@pulumi.output_type
class GetFoldersResult:
    """
    A collection of values returned by getFolders.
    """
    def __init__(__self__, enable_details=None, folders=None, id=None, ids=None, name_regex=None, names=None, output_file=None, parent_folder_id=None, query_keyword=None):
        if enable_details and not isinstance(enable_details, bool):
            raise TypeError("Expected argument 'enable_details' to be a bool")
        pulumi.set(__self__, "enable_details", enable_details)
        if folders and not isinstance(folders, list):
            raise TypeError("Expected argument 'folders' to be a list")
        pulumi.set(__self__, "folders", folders)
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
        if parent_folder_id and not isinstance(parent_folder_id, str):
            raise TypeError("Expected argument 'parent_folder_id' to be a str")
        pulumi.set(__self__, "parent_folder_id", parent_folder_id)
        if query_keyword and not isinstance(query_keyword, str):
            raise TypeError("Expected argument 'query_keyword' to be a str")
        pulumi.set(__self__, "query_keyword", query_keyword)

    @property
    @pulumi.getter(name="enableDetails")
    def enable_details(self) -> Optional[bool]:
        return pulumi.get(self, "enable_details")

    @property
    @pulumi.getter
    def folders(self) -> Sequence['outputs.GetFoldersFolderResult']:
        """
        A list of folders. Each element contains the following attributes:
        """
        return pulumi.get(self, "folders")

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
        A list of folder IDs.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        """
        A list of folder names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="parentFolderId")
    def parent_folder_id(self) -> Optional[str]:
        """
        (Available in v1.114.0+)The ID of the parent folder.
        """
        return pulumi.get(self, "parent_folder_id")

    @property
    @pulumi.getter(name="queryKeyword")
    def query_keyword(self) -> Optional[str]:
        return pulumi.get(self, "query_keyword")


class AwaitableGetFoldersResult(GetFoldersResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFoldersResult(
            enable_details=self.enable_details,
            folders=self.folders,
            id=self.id,
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            parent_folder_id=self.parent_folder_id,
            query_keyword=self.query_keyword)


def get_folders(enable_details: Optional[bool] = None,
                ids: Optional[Sequence[str]] = None,
                name_regex: Optional[str] = None,
                output_file: Optional[str] = None,
                parent_folder_id: Optional[str] = None,
                query_keyword: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFoldersResult:
    """
    This data source provides the resource manager folders of the current Alibaba Cloud user.

    > **NOTE:**  Available in 1.84.0+.

    > **NOTE:**  You can view only the information of the first-level child folders of the specified folder.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.resourcemanager.get_folders(name_regex="tftest")
    pulumi.export("firstFolderId", example.folders[0].id)
    ```


    :param bool enable_details: Default to `false`. Set it to true can output more details.
    :param Sequence[str] ids: A list of resource manager folders IDs.
    :param str name_regex: A regex string to filter results by folder name.
    :param str parent_folder_id: The ID of the parent folder.
    :param str query_keyword: The query keyword.
    """
    __args__ = dict()
    __args__['enableDetails'] = enable_details
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['parentFolderId'] = parent_folder_id
    __args__['queryKeyword'] = query_keyword
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:resourcemanager/getFolders:getFolders', __args__, opts=opts, typ=GetFoldersResult).value

    return AwaitableGetFoldersResult(
        enable_details=__ret__.enable_details,
        folders=__ret__.folders,
        id=__ret__.id,
        ids=__ret__.ids,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file,
        parent_folder_id=__ret__.parent_folder_id,
        query_keyword=__ret__.query_keyword)


@_utilities.lift_output_func(get_folders)
def get_folders_output(enable_details: Optional[pulumi.Input[Optional[bool]]] = None,
                       ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                       name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                       output_file: Optional[pulumi.Input[Optional[str]]] = None,
                       parent_folder_id: Optional[pulumi.Input[Optional[str]]] = None,
                       query_keyword: Optional[pulumi.Input[Optional[str]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFoldersResult]:
    """
    This data source provides the resource manager folders of the current Alibaba Cloud user.

    > **NOTE:**  Available in 1.84.0+.

    > **NOTE:**  You can view only the information of the first-level child folders of the specified folder.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.resourcemanager.get_folders(name_regex="tftest")
    pulumi.export("firstFolderId", example.folders[0].id)
    ```


    :param bool enable_details: Default to `false`. Set it to true can output more details.
    :param Sequence[str] ids: A list of resource manager folders IDs.
    :param str name_regex: A regex string to filter results by folder name.
    :param str parent_folder_id: The ID of the parent folder.
    :param str query_keyword: The query keyword.
    """
    ...
