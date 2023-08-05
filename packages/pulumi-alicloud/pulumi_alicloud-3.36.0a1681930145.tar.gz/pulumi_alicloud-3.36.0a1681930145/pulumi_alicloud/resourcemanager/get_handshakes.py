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
    'GetHandshakesResult',
    'AwaitableGetHandshakesResult',
    'get_handshakes',
    'get_handshakes_output',
]

@pulumi.output_type
class GetHandshakesResult:
    """
    A collection of values returned by getHandshakes.
    """
    def __init__(__self__, enable_details=None, handshakes=None, id=None, ids=None, output_file=None, status=None):
        if enable_details and not isinstance(enable_details, bool):
            raise TypeError("Expected argument 'enable_details' to be a bool")
        pulumi.set(__self__, "enable_details", enable_details)
        if handshakes and not isinstance(handshakes, list):
            raise TypeError("Expected argument 'handshakes' to be a list")
        pulumi.set(__self__, "handshakes", handshakes)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="enableDetails")
    def enable_details(self) -> Optional[bool]:
        return pulumi.get(self, "enable_details")

    @property
    @pulumi.getter
    def handshakes(self) -> Sequence['outputs.GetHandshakesHandshakeResult']:
        """
        A list of Resource Manager Handshakes. Each element contains the following attributes:
        """
        return pulumi.get(self, "handshakes")

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
        A list of Resource Manager Handshake IDs.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The status of the invitation.
        """
        return pulumi.get(self, "status")


class AwaitableGetHandshakesResult(GetHandshakesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetHandshakesResult(
            enable_details=self.enable_details,
            handshakes=self.handshakes,
            id=self.id,
            ids=self.ids,
            output_file=self.output_file,
            status=self.status)


def get_handshakes(enable_details: Optional[bool] = None,
                   ids: Optional[Sequence[str]] = None,
                   output_file: Optional[str] = None,
                   status: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetHandshakesResult:
    """
    This data source provides the Resource Manager Handshakes of the current Alibaba Cloud user.

    > **NOTE:**  Available in 1.86.0+.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.resourcemanager.get_handshakes()
    pulumi.export("firstHandshakeId", example.handshakes[0].id)
    ```


    :param bool enable_details: Default to `false`. Set it to true can output more details.
    :param Sequence[str] ids: A list of Resource Manager Handshake IDs.
    :param str status: The status of handshake, valid values: `Accepted`, `Cancelled`, `Declined`, `Deleted`, `Expired` and `Pending`.
    """
    __args__ = dict()
    __args__['enableDetails'] = enable_details
    __args__['ids'] = ids
    __args__['outputFile'] = output_file
    __args__['status'] = status
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:resourcemanager/getHandshakes:getHandshakes', __args__, opts=opts, typ=GetHandshakesResult).value

    return AwaitableGetHandshakesResult(
        enable_details=__ret__.enable_details,
        handshakes=__ret__.handshakes,
        id=__ret__.id,
        ids=__ret__.ids,
        output_file=__ret__.output_file,
        status=__ret__.status)


@_utilities.lift_output_func(get_handshakes)
def get_handshakes_output(enable_details: Optional[pulumi.Input[Optional[bool]]] = None,
                          ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                          output_file: Optional[pulumi.Input[Optional[str]]] = None,
                          status: Optional[pulumi.Input[Optional[str]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetHandshakesResult]:
    """
    This data source provides the Resource Manager Handshakes of the current Alibaba Cloud user.

    > **NOTE:**  Available in 1.86.0+.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.resourcemanager.get_handshakes()
    pulumi.export("firstHandshakeId", example.handshakes[0].id)
    ```


    :param bool enable_details: Default to `false`. Set it to true can output more details.
    :param Sequence[str] ids: A list of Resource Manager Handshake IDs.
    :param str status: The status of handshake, valid values: `Accepted`, `Cancelled`, `Declined`, `Deleted`, `Expired` and `Pending`.
    """
    ...
