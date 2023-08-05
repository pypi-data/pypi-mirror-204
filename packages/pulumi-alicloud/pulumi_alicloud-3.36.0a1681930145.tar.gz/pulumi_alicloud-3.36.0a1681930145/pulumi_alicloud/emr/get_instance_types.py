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
    'GetInstanceTypesResult',
    'AwaitableGetInstanceTypesResult',
    'get_instance_types',
    'get_instance_types_output',
]

@pulumi.output_type
class GetInstanceTypesResult:
    """
    A collection of values returned by getInstanceTypes.
    """
    def __init__(__self__, cluster_type=None, destination_resource=None, id=None, ids=None, instance_charge_type=None, instance_type=None, output_file=None, support_local_storage=None, support_node_types=None, types=None, zone_id=None):
        if cluster_type and not isinstance(cluster_type, str):
            raise TypeError("Expected argument 'cluster_type' to be a str")
        pulumi.set(__self__, "cluster_type", cluster_type)
        if destination_resource and not isinstance(destination_resource, str):
            raise TypeError("Expected argument 'destination_resource' to be a str")
        pulumi.set(__self__, "destination_resource", destination_resource)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if instance_charge_type and not isinstance(instance_charge_type, str):
            raise TypeError("Expected argument 'instance_charge_type' to be a str")
        pulumi.set(__self__, "instance_charge_type", instance_charge_type)
        if instance_type and not isinstance(instance_type, str):
            raise TypeError("Expected argument 'instance_type' to be a str")
        pulumi.set(__self__, "instance_type", instance_type)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if support_local_storage and not isinstance(support_local_storage, bool):
            raise TypeError("Expected argument 'support_local_storage' to be a bool")
        pulumi.set(__self__, "support_local_storage", support_local_storage)
        if support_node_types and not isinstance(support_node_types, list):
            raise TypeError("Expected argument 'support_node_types' to be a list")
        pulumi.set(__self__, "support_node_types", support_node_types)
        if types and not isinstance(types, list):
            raise TypeError("Expected argument 'types' to be a list")
        pulumi.set(__self__, "types", types)
        if zone_id and not isinstance(zone_id, str):
            raise TypeError("Expected argument 'zone_id' to be a str")
        pulumi.set(__self__, "zone_id", zone_id)

    @property
    @pulumi.getter(name="clusterType")
    def cluster_type(self) -> str:
        return pulumi.get(self, "cluster_type")

    @property
    @pulumi.getter(name="destinationResource")
    def destination_resource(self) -> str:
        return pulumi.get(self, "destination_resource")

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
        A list of emr instance types IDs.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="instanceChargeType")
    def instance_charge_type(self) -> str:
        return pulumi.get(self, "instance_charge_type")

    @property
    @pulumi.getter(name="instanceType")
    def instance_type(self) -> Optional[str]:
        return pulumi.get(self, "instance_type")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="supportLocalStorage")
    def support_local_storage(self) -> Optional[bool]:
        return pulumi.get(self, "support_local_storage")

    @property
    @pulumi.getter(name="supportNodeTypes")
    def support_node_types(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "support_node_types")

    @property
    @pulumi.getter
    def types(self) -> Sequence['outputs.GetInstanceTypesTypeResult']:
        """
        A list of emr instance types. Each element contains the following attributes:
        """
        return pulumi.get(self, "types")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> Optional[str]:
        """
        The available zone id in Alibaba Cloud account
        """
        return pulumi.get(self, "zone_id")


class AwaitableGetInstanceTypesResult(GetInstanceTypesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstanceTypesResult(
            cluster_type=self.cluster_type,
            destination_resource=self.destination_resource,
            id=self.id,
            ids=self.ids,
            instance_charge_type=self.instance_charge_type,
            instance_type=self.instance_type,
            output_file=self.output_file,
            support_local_storage=self.support_local_storage,
            support_node_types=self.support_node_types,
            types=self.types,
            zone_id=self.zone_id)


def get_instance_types(cluster_type: Optional[str] = None,
                       destination_resource: Optional[str] = None,
                       instance_charge_type: Optional[str] = None,
                       instance_type: Optional[str] = None,
                       output_file: Optional[str] = None,
                       support_local_storage: Optional[bool] = None,
                       support_node_types: Optional[Sequence[str]] = None,
                       zone_id: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstanceTypesResult:
    """
    The _emr_get_instance_types_ data source provides a collection of ecs
    instance types available in Alibaba Cloud account when create a emr cluster.

    > **NOTE:** Available in 1.59.0+

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.emr.get_instance_types(cluster_type="HADOOP",
        destination_resource="InstanceType",
        instance_charge_type="PostPaid",
        instance_type="ecs.g5.2xlarge",
        support_local_storage=False,
        support_node_types=[
            "MASTER",
            "CORE",
        ])
    pulumi.export("firstInstanceType", default.types[0].id)
    ```


    :param str cluster_type: The cluster type of the emr cluster instance. Possible values: `HADOOP`, `KAFKA`, `ZOOKEEPER`, `DRUID`.
    :param str destination_resource: The destination resource of emr cluster instance
    :param str instance_charge_type: Filter the results by charge type. Valid values: `PrePaid` and `PostPaid`. Default to `PostPaid`.
    :param str instance_type: Filter the specific ecs instance type to create emr cluster.
    :param bool support_local_storage: Whether the current storage disk is local or not.
    :param Sequence[str] support_node_types: The specific supported node type list.
           Possible values may be any one or combination of these: ["MASTER", "CORE", "TASK", "GATEWAY"]
    :param str zone_id: The supported resources of specific zoneId.
    """
    __args__ = dict()
    __args__['clusterType'] = cluster_type
    __args__['destinationResource'] = destination_resource
    __args__['instanceChargeType'] = instance_charge_type
    __args__['instanceType'] = instance_type
    __args__['outputFile'] = output_file
    __args__['supportLocalStorage'] = support_local_storage
    __args__['supportNodeTypes'] = support_node_types
    __args__['zoneId'] = zone_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:emr/getInstanceTypes:getInstanceTypes', __args__, opts=opts, typ=GetInstanceTypesResult).value

    return AwaitableGetInstanceTypesResult(
        cluster_type=__ret__.cluster_type,
        destination_resource=__ret__.destination_resource,
        id=__ret__.id,
        ids=__ret__.ids,
        instance_charge_type=__ret__.instance_charge_type,
        instance_type=__ret__.instance_type,
        output_file=__ret__.output_file,
        support_local_storage=__ret__.support_local_storage,
        support_node_types=__ret__.support_node_types,
        types=__ret__.types,
        zone_id=__ret__.zone_id)


@_utilities.lift_output_func(get_instance_types)
def get_instance_types_output(cluster_type: Optional[pulumi.Input[str]] = None,
                              destination_resource: Optional[pulumi.Input[str]] = None,
                              instance_charge_type: Optional[pulumi.Input[str]] = None,
                              instance_type: Optional[pulumi.Input[Optional[str]]] = None,
                              output_file: Optional[pulumi.Input[Optional[str]]] = None,
                              support_local_storage: Optional[pulumi.Input[Optional[bool]]] = None,
                              support_node_types: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                              zone_id: Optional[pulumi.Input[Optional[str]]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInstanceTypesResult]:
    """
    The _emr_get_instance_types_ data source provides a collection of ecs
    instance types available in Alibaba Cloud account when create a emr cluster.

    > **NOTE:** Available in 1.59.0+

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.emr.get_instance_types(cluster_type="HADOOP",
        destination_resource="InstanceType",
        instance_charge_type="PostPaid",
        instance_type="ecs.g5.2xlarge",
        support_local_storage=False,
        support_node_types=[
            "MASTER",
            "CORE",
        ])
    pulumi.export("firstInstanceType", default.types[0].id)
    ```


    :param str cluster_type: The cluster type of the emr cluster instance. Possible values: `HADOOP`, `KAFKA`, `ZOOKEEPER`, `DRUID`.
    :param str destination_resource: The destination resource of emr cluster instance
    :param str instance_charge_type: Filter the results by charge type. Valid values: `PrePaid` and `PostPaid`. Default to `PostPaid`.
    :param str instance_type: Filter the specific ecs instance type to create emr cluster.
    :param bool support_local_storage: Whether the current storage disk is local or not.
    :param Sequence[str] support_node_types: The specific supported node type list.
           Possible values may be any one or combination of these: ["MASTER", "CORE", "TASK", "GATEWAY"]
    :param str zone_id: The supported resources of specific zoneId.
    """
    ...
