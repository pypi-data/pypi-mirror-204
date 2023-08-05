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
    def __init__(__self__, enable_details=None, id=None, ids=None, image_id=None, instance_name=None, instance_type=None, instances=None, key_pair_name=None, name_regex=None, names=None, output_file=None, payment_type=None, resolution=None, status=None, zone_id=None):
        if enable_details and not isinstance(enable_details, bool):
            raise TypeError("Expected argument 'enable_details' to be a bool")
        pulumi.set(__self__, "enable_details", enable_details)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if image_id and not isinstance(image_id, str):
            raise TypeError("Expected argument 'image_id' to be a str")
        pulumi.set(__self__, "image_id", image_id)
        if instance_name and not isinstance(instance_name, str):
            raise TypeError("Expected argument 'instance_name' to be a str")
        pulumi.set(__self__, "instance_name", instance_name)
        if instance_type and not isinstance(instance_type, str):
            raise TypeError("Expected argument 'instance_type' to be a str")
        pulumi.set(__self__, "instance_type", instance_type)
        if instances and not isinstance(instances, list):
            raise TypeError("Expected argument 'instances' to be a list")
        pulumi.set(__self__, "instances", instances)
        if key_pair_name and not isinstance(key_pair_name, str):
            raise TypeError("Expected argument 'key_pair_name' to be a str")
        pulumi.set(__self__, "key_pair_name", key_pair_name)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if payment_type and not isinstance(payment_type, str):
            raise TypeError("Expected argument 'payment_type' to be a str")
        pulumi.set(__self__, "payment_type", payment_type)
        if resolution and not isinstance(resolution, str):
            raise TypeError("Expected argument 'resolution' to be a str")
        pulumi.set(__self__, "resolution", resolution)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if zone_id and not isinstance(zone_id, str):
            raise TypeError("Expected argument 'zone_id' to be a str")
        pulumi.set(__self__, "zone_id", zone_id)

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
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="imageId")
    def image_id(self) -> Optional[str]:
        return pulumi.get(self, "image_id")

    @property
    @pulumi.getter(name="instanceName")
    def instance_name(self) -> Optional[str]:
        return pulumi.get(self, "instance_name")

    @property
    @pulumi.getter(name="instanceType")
    def instance_type(self) -> Optional[str]:
        return pulumi.get(self, "instance_type")

    @property
    @pulumi.getter
    def instances(self) -> Sequence['outputs.GetInstancesInstanceResult']:
        return pulumi.get(self, "instances")

    @property
    @pulumi.getter(name="keyPairName")
    def key_pair_name(self) -> Optional[str]:
        return pulumi.get(self, "key_pair_name")

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

    @property
    @pulumi.getter(name="paymentType")
    def payment_type(self) -> Optional[str]:
        return pulumi.get(self, "payment_type")

    @property
    @pulumi.getter
    def resolution(self) -> Optional[str]:
        return pulumi.get(self, "resolution")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> Optional[str]:
        return pulumi.get(self, "zone_id")


class AwaitableGetInstancesResult(GetInstancesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstancesResult(
            enable_details=self.enable_details,
            id=self.id,
            ids=self.ids,
            image_id=self.image_id,
            instance_name=self.instance_name,
            instance_type=self.instance_type,
            instances=self.instances,
            key_pair_name=self.key_pair_name,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            payment_type=self.payment_type,
            resolution=self.resolution,
            status=self.status,
            zone_id=self.zone_id)


def get_instances(enable_details: Optional[bool] = None,
                  ids: Optional[Sequence[str]] = None,
                  image_id: Optional[str] = None,
                  instance_name: Optional[str] = None,
                  instance_type: Optional[str] = None,
                  key_pair_name: Optional[str] = None,
                  name_regex: Optional[str] = None,
                  output_file: Optional[str] = None,
                  payment_type: Optional[str] = None,
                  resolution: Optional[str] = None,
                  status: Optional[str] = None,
                  zone_id: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstancesResult:
    """
    This data source provides the Ecp Instances of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.158.0+.


    :param Sequence[str] ids: A list of Ecp Instances IDs.
    :param str image_id: The ID Of The Image.
    :param str instance_name: Instance Name.
    :param str instance_type: Instance Type.
    :param str key_pair_name: The Key Name.
    :param str name_regex: A regex string to filter results by mobile phone name.
    :param str payment_type: The payment type.Valid values: `PayAsYouGo`,`Subscription`
    :param str resolution: Resolution.
    :param str status: Instance Status.
    """
    __args__ = dict()
    __args__['enableDetails'] = enable_details
    __args__['ids'] = ids
    __args__['imageId'] = image_id
    __args__['instanceName'] = instance_name
    __args__['instanceType'] = instance_type
    __args__['keyPairName'] = key_pair_name
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['paymentType'] = payment_type
    __args__['resolution'] = resolution
    __args__['status'] = status
    __args__['zoneId'] = zone_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:ecp/getInstances:getInstances', __args__, opts=opts, typ=GetInstancesResult).value

    return AwaitableGetInstancesResult(
        enable_details=__ret__.enable_details,
        id=__ret__.id,
        ids=__ret__.ids,
        image_id=__ret__.image_id,
        instance_name=__ret__.instance_name,
        instance_type=__ret__.instance_type,
        instances=__ret__.instances,
        key_pair_name=__ret__.key_pair_name,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file,
        payment_type=__ret__.payment_type,
        resolution=__ret__.resolution,
        status=__ret__.status,
        zone_id=__ret__.zone_id)


@_utilities.lift_output_func(get_instances)
def get_instances_output(enable_details: Optional[pulumi.Input[Optional[bool]]] = None,
                         ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                         image_id: Optional[pulumi.Input[Optional[str]]] = None,
                         instance_name: Optional[pulumi.Input[Optional[str]]] = None,
                         instance_type: Optional[pulumi.Input[Optional[str]]] = None,
                         key_pair_name: Optional[pulumi.Input[Optional[str]]] = None,
                         name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                         output_file: Optional[pulumi.Input[Optional[str]]] = None,
                         payment_type: Optional[pulumi.Input[Optional[str]]] = None,
                         resolution: Optional[pulumi.Input[Optional[str]]] = None,
                         status: Optional[pulumi.Input[Optional[str]]] = None,
                         zone_id: Optional[pulumi.Input[Optional[str]]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInstancesResult]:
    """
    This data source provides the Ecp Instances of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.158.0+.


    :param Sequence[str] ids: A list of Ecp Instances IDs.
    :param str image_id: The ID Of The Image.
    :param str instance_name: Instance Name.
    :param str instance_type: Instance Type.
    :param str key_pair_name: The Key Name.
    :param str name_regex: A regex string to filter results by mobile phone name.
    :param str payment_type: The payment type.Valid values: `PayAsYouGo`,`Subscription`
    :param str resolution: Resolution.
    :param str status: Instance Status.
    """
    ...
