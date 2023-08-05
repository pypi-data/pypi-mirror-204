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
    'GetInstancesResult',
    'AwaitableGetInstancesResult',
    'get_instances',
    'get_instances_output',
]

@pulumi.output_type
class GetInstancesResult:
    """
    A collection of values returned by getInstances.
    """
    def __init__(__self__, description_regex=None, descriptions=None, id=None, ids=None, instances=None, output_file=None, tags=None):
        if description_regex and not isinstance(description_regex, str):
            raise TypeError("Expected argument 'description_regex' to be a str")
        pulumi.set(__self__, "description_regex", description_regex)
        if descriptions and not isinstance(descriptions, list):
            raise TypeError("Expected argument 'descriptions' to be a list")
        pulumi.set(__self__, "descriptions", descriptions)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if instances and not isinstance(instances, list):
            raise TypeError("Expected argument 'instances' to be a list")
        pulumi.set(__self__, "instances", instances)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="descriptionRegex")
    def description_regex(self) -> Optional[str]:
        return pulumi.get(self, "description_regex")

    @property
    @pulumi.getter
    def descriptions(self) -> Sequence[str]:
        return pulumi.get(self, "descriptions")

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
    def instances(self) -> Sequence['outputs.GetInstancesInstanceResult']:
        """
        A list of apis. Each element contains the following attributes:
        """
        return pulumi.get(self, "instances")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, Any]]:
        """
        A map of tags assigned to the bastionhost instance.
        """
        return pulumi.get(self, "tags")


class AwaitableGetInstancesResult(GetInstancesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstancesResult(
            description_regex=self.description_regex,
            descriptions=self.descriptions,
            id=self.id,
            ids=self.ids,
            instances=self.instances,
            output_file=self.output_file,
            tags=self.tags)


def get_instances(description_regex: Optional[str] = None,
                  ids: Optional[Sequence[str]] = None,
                  output_file: Optional[str] = None,
                  tags: Optional[Mapping[str, Any]] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstancesResult:
    """
    > **NOTE:** From the version 1.132.0, the data source has been renamed to _bastionhost_get_instances_.

    This data source provides a list of cloud Bastionhost instances in an Alibaba Cloud account according to the specified filters.

    > **NOTE:** Available in 1.63.0+ .

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    instance_instances = alicloud.bastionhost.get_instances(description_regex="^bastionhost")
    pulumi.export("instance", [__item["id"] for __item in alicloud_bastionhost_instances["instance"]])
    ```


    :param str description_regex: A regex string to filter results by the instance description.
    :param Sequence[str] ids: Matched instance IDs to filter data source result.
    :param str output_file: File name to persist data source output.
    :param Mapping[str, Any] tags: A map of tags assigned to the bastionhost instance. It must be in the format:
           ```python
           import pulumi
           import pulumi_alicloud as alicloud
           
           instance = alicloud.bastionhost.get_instances(tags={
               "tagKey1": "tagValue1",
           })
           ```
    """
    __args__ = dict()
    __args__['descriptionRegex'] = description_regex
    __args__['ids'] = ids
    __args__['outputFile'] = output_file
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:bastionhost/getInstances:getInstances', __args__, opts=opts, typ=GetInstancesResult).value

    return AwaitableGetInstancesResult(
        description_regex=__ret__.description_regex,
        descriptions=__ret__.descriptions,
        id=__ret__.id,
        ids=__ret__.ids,
        instances=__ret__.instances,
        output_file=__ret__.output_file,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_instances)
def get_instances_output(description_regex: Optional[pulumi.Input[Optional[str]]] = None,
                         ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                         output_file: Optional[pulumi.Input[Optional[str]]] = None,
                         tags: Optional[pulumi.Input[Optional[Mapping[str, Any]]]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInstancesResult]:
    """
    > **NOTE:** From the version 1.132.0, the data source has been renamed to _bastionhost_get_instances_.

    This data source provides a list of cloud Bastionhost instances in an Alibaba Cloud account according to the specified filters.

    > **NOTE:** Available in 1.63.0+ .

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    instance_instances = alicloud.bastionhost.get_instances(description_regex="^bastionhost")
    pulumi.export("instance", [__item["id"] for __item in alicloud_bastionhost_instances["instance"]])
    ```


    :param str description_regex: A regex string to filter results by the instance description.
    :param Sequence[str] ids: Matched instance IDs to filter data source result.
    :param str output_file: File name to persist data source output.
    :param Mapping[str, Any] tags: A map of tags assigned to the bastionhost instance. It must be in the format:
           ```python
           import pulumi
           import pulumi_alicloud as alicloud
           
           instance = alicloud.bastionhost.get_instances(tags={
               "tagKey1": "tagValue1",
           })
           ```
    """
    ...
