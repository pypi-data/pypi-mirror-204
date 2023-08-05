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
    'GetVpcEndpointLinkedVpcsResult',
    'AwaitableGetVpcEndpointLinkedVpcsResult',
    'get_vpc_endpoint_linked_vpcs',
    'get_vpc_endpoint_linked_vpcs_output',
]

@pulumi.output_type
class GetVpcEndpointLinkedVpcsResult:
    """
    A collection of values returned by getVpcEndpointLinkedVpcs.
    """
    def __init__(__self__, id=None, ids=None, instance_id=None, module_name=None, output_file=None, status=None, vpc_endpoint_linked_vpcs=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if instance_id and not isinstance(instance_id, str):
            raise TypeError("Expected argument 'instance_id' to be a str")
        pulumi.set(__self__, "instance_id", instance_id)
        if module_name and not isinstance(module_name, str):
            raise TypeError("Expected argument 'module_name' to be a str")
        pulumi.set(__self__, "module_name", module_name)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if vpc_endpoint_linked_vpcs and not isinstance(vpc_endpoint_linked_vpcs, list):
            raise TypeError("Expected argument 'vpc_endpoint_linked_vpcs' to be a list")
        pulumi.set(__self__, "vpc_endpoint_linked_vpcs", vpc_endpoint_linked_vpcs)

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
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> str:
        """
        The ID of the instance.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="moduleName")
    def module_name(self) -> str:
        """
        The name of the module that you want to access.
        """
        return pulumi.get(self, "module_name")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The status of the Vpc Endpoint Linked Vpc.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="vpcEndpointLinkedVpcs")
    def vpc_endpoint_linked_vpcs(self) -> Sequence['outputs.GetVpcEndpointLinkedVpcsVpcEndpointLinkedVpcResult']:
        """
        A list of CR Vpc Endpoint Linked Vpcs. Each element contains the following attributes:
        """
        return pulumi.get(self, "vpc_endpoint_linked_vpcs")


class AwaitableGetVpcEndpointLinkedVpcsResult(GetVpcEndpointLinkedVpcsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVpcEndpointLinkedVpcsResult(
            id=self.id,
            ids=self.ids,
            instance_id=self.instance_id,
            module_name=self.module_name,
            output_file=self.output_file,
            status=self.status,
            vpc_endpoint_linked_vpcs=self.vpc_endpoint_linked_vpcs)


def get_vpc_endpoint_linked_vpcs(ids: Optional[Sequence[str]] = None,
                                 instance_id: Optional[str] = None,
                                 module_name: Optional[str] = None,
                                 output_file: Optional[str] = None,
                                 status: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVpcEndpointLinkedVpcsResult:
    """
    This data source provides the CR Vpc Endpoint Linked Vpcs of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.199.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.cr.get_vpc_endpoint_linked_vpcs(ids=["example_id"],
        instance_id="your_cr_instance_id",
        module_name="Registry")
    pulumi.export("alicloudCrVpcEndpointLinkedVpcsId1", ids.vpc_endpoint_linked_vpcs[0].id)
    ```


    :param Sequence[str] ids: A list of CR Vpc Endpoint Linked Vpc IDs.
    :param str instance_id: The ID of the instance.
    :param str module_name: The name of the module that you want to access. Valid Values:
    :param str status: The status of the Vpc Endpoint Linked Vpc. Valid Values: `CREATING`, `RUNNING`.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['instanceId'] = instance_id
    __args__['moduleName'] = module_name
    __args__['outputFile'] = output_file
    __args__['status'] = status
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:cr/getVpcEndpointLinkedVpcs:getVpcEndpointLinkedVpcs', __args__, opts=opts, typ=GetVpcEndpointLinkedVpcsResult).value

    return AwaitableGetVpcEndpointLinkedVpcsResult(
        id=__ret__.id,
        ids=__ret__.ids,
        instance_id=__ret__.instance_id,
        module_name=__ret__.module_name,
        output_file=__ret__.output_file,
        status=__ret__.status,
        vpc_endpoint_linked_vpcs=__ret__.vpc_endpoint_linked_vpcs)


@_utilities.lift_output_func(get_vpc_endpoint_linked_vpcs)
def get_vpc_endpoint_linked_vpcs_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                        instance_id: Optional[pulumi.Input[str]] = None,
                                        module_name: Optional[pulumi.Input[str]] = None,
                                        output_file: Optional[pulumi.Input[Optional[str]]] = None,
                                        status: Optional[pulumi.Input[Optional[str]]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVpcEndpointLinkedVpcsResult]:
    """
    This data source provides the CR Vpc Endpoint Linked Vpcs of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.199.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.cr.get_vpc_endpoint_linked_vpcs(ids=["example_id"],
        instance_id="your_cr_instance_id",
        module_name="Registry")
    pulumi.export("alicloudCrVpcEndpointLinkedVpcsId1", ids.vpc_endpoint_linked_vpcs[0].id)
    ```


    :param Sequence[str] ids: A list of CR Vpc Endpoint Linked Vpc IDs.
    :param str instance_id: The ID of the instance.
    :param str module_name: The name of the module that you want to access. Valid Values:
    :param str status: The status of the Vpc Endpoint Linked Vpc. Valid Values: `CREATING`, `RUNNING`.
    """
    ...
