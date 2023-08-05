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
    'GetDdosBgpInstancesResult',
    'AwaitableGetDdosBgpInstancesResult',
    'get_ddos_bgp_instances',
    'get_ddos_bgp_instances_output',
]

@pulumi.output_type
class GetDdosBgpInstancesResult:
    """
    A collection of values returned by getDdosBgpInstances.
    """
    def __init__(__self__, id=None, ids=None, instances=None, name_regex=None, names=None, output_file=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if instances and not isinstance(instances, list):
            raise TypeError("Expected argument 'instances' to be a list")
        pulumi.set(__self__, "instances", instances)
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
        A list of instance IDs.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter
    def instances(self) -> Sequence['outputs.GetDdosBgpInstancesInstanceResult']:
        """
        A list of apis. Each element contains the following attributes:
        """
        return pulumi.get(self, "instances")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        """
        A list of instance names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")


class AwaitableGetDdosBgpInstancesResult(GetDdosBgpInstancesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDdosBgpInstancesResult(
            id=self.id,
            ids=self.ids,
            instances=self.instances,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file)


def get_ddos_bgp_instances(ids: Optional[Sequence[str]] = None,
                           name_regex: Optional[str] = None,
                           output_file: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDdosBgpInstancesResult:
    """
    This data source provides a list of Anti-DDoS Advanced instances in an Alibaba Cloud account according to the specified filters.

    > **NOTE:** Available in 1.183.0+ .

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    instance_ddos_bgp_instances = alicloud.ddos.get_ddos_bgp_instances(name_regex="^ddosbgp")
    pulumi.export("instance", [__item["id"] for __item in alicloud_ddosbgp_instances["instance"]])
    ```


    :param Sequence[str] ids: A list of instance IDs.
    :param str name_regex: A regex string to filter results by the instance name.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:ddos/getDdosBgpInstances:getDdosBgpInstances', __args__, opts=opts, typ=GetDdosBgpInstancesResult).value

    return AwaitableGetDdosBgpInstancesResult(
        id=__ret__.id,
        ids=__ret__.ids,
        instances=__ret__.instances,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file)


@_utilities.lift_output_func(get_ddos_bgp_instances)
def get_ddos_bgp_instances_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                  name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                                  output_file: Optional[pulumi.Input[Optional[str]]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDdosBgpInstancesResult]:
    """
    This data source provides a list of Anti-DDoS Advanced instances in an Alibaba Cloud account according to the specified filters.

    > **NOTE:** Available in 1.183.0+ .

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    instance_ddos_bgp_instances = alicloud.ddos.get_ddos_bgp_instances(name_regex="^ddosbgp")
    pulumi.export("instance", [__item["id"] for __item in alicloud_ddosbgp_instances["instance"]])
    ```


    :param Sequence[str] ids: A list of instance IDs.
    :param str name_regex: A regex string to filter results by the instance name.
    """
    ...
