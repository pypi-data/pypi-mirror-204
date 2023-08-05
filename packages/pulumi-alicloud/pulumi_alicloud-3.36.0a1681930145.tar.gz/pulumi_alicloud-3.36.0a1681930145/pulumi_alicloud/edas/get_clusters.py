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
    'GetClustersResult',
    'AwaitableGetClustersResult',
    'get_clusters',
    'get_clusters_output',
]

@pulumi.output_type
class GetClustersResult:
    """
    A collection of values returned by getClusters.
    """
    def __init__(__self__, clusters=None, id=None, ids=None, logical_region_id=None, name_regex=None, names=None, output_file=None):
        if clusters and not isinstance(clusters, list):
            raise TypeError("Expected argument 'clusters' to be a list")
        pulumi.set(__self__, "clusters", clusters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if logical_region_id and not isinstance(logical_region_id, str):
            raise TypeError("Expected argument 'logical_region_id' to be a str")
        pulumi.set(__self__, "logical_region_id", logical_region_id)
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
    def clusters(self) -> Sequence['outputs.GetClustersClusterResult']:
        """
        A list of clusters.
        """
        return pulumi.get(self, "clusters")

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
        A list of cluster IDs.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="logicalRegionId")
    def logical_region_id(self) -> str:
        return pulumi.get(self, "logical_region_id")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        """
        A list of cluster names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")


class AwaitableGetClustersResult(GetClustersResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetClustersResult(
            clusters=self.clusters,
            id=self.id,
            ids=self.ids,
            logical_region_id=self.logical_region_id,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file)


def get_clusters(ids: Optional[Sequence[str]] = None,
                 logical_region_id: Optional[str] = None,
                 name_regex: Optional[str] = None,
                 output_file: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetClustersResult:
    """
    This data source provides a list of EDAS clusters in an Alibaba Cloud account according to the specified filters.

    > **NOTE:** Available in 1.82.0+

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    clusters = alicloud.edas.get_clusters(logical_region_id="cn-shenzhen:xxx",
        ids=["addfs-dfsasd"],
        output_file="clusters.txt")
    pulumi.export("firstClusterName", data["alicloud_alikafka_consumer_groups"]["clusters"]["clusters"][0]["cluster_name"])
    ```


    :param Sequence[str] ids: An ids string to filter results by the cluster id.
    :param str logical_region_id: ID of the namespace in EDAS.
    :param str name_regex: A regex string to filter results by the cluster name.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['logicalRegionId'] = logical_region_id
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:edas/getClusters:getClusters', __args__, opts=opts, typ=GetClustersResult).value

    return AwaitableGetClustersResult(
        clusters=__ret__.clusters,
        id=__ret__.id,
        ids=__ret__.ids,
        logical_region_id=__ret__.logical_region_id,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file)


@_utilities.lift_output_func(get_clusters)
def get_clusters_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                        logical_region_id: Optional[pulumi.Input[str]] = None,
                        name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                        output_file: Optional[pulumi.Input[Optional[str]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetClustersResult]:
    """
    This data source provides a list of EDAS clusters in an Alibaba Cloud account according to the specified filters.

    > **NOTE:** Available in 1.82.0+

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    clusters = alicloud.edas.get_clusters(logical_region_id="cn-shenzhen:xxx",
        ids=["addfs-dfsasd"],
        output_file="clusters.txt")
    pulumi.export("firstClusterName", data["alicloud_alikafka_consumer_groups"]["clusters"]["clusters"][0]["cluster_name"])
    ```


    :param Sequence[str] ids: An ids string to filter results by the cluster id.
    :param str logical_region_id: ID of the namespace in EDAS.
    :param str name_regex: A regex string to filter results by the cluster name.
    """
    ...
