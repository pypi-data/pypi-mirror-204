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
    'GetTransitRouterVbrAttachmentsResult',
    'AwaitableGetTransitRouterVbrAttachmentsResult',
    'get_transit_router_vbr_attachments',
    'get_transit_router_vbr_attachments_output',
]

@pulumi.output_type
class GetTransitRouterVbrAttachmentsResult:
    """
    A collection of values returned by getTransitRouterVbrAttachments.
    """
    def __init__(__self__, attachments=None, cen_id=None, id=None, ids=None, output_file=None, status=None, transit_router_id=None):
        if attachments and not isinstance(attachments, list):
            raise TypeError("Expected argument 'attachments' to be a list")
        pulumi.set(__self__, "attachments", attachments)
        if cen_id and not isinstance(cen_id, str):
            raise TypeError("Expected argument 'cen_id' to be a str")
        pulumi.set(__self__, "cen_id", cen_id)
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
        if transit_router_id and not isinstance(transit_router_id, str):
            raise TypeError("Expected argument 'transit_router_id' to be a str")
        pulumi.set(__self__, "transit_router_id", transit_router_id)

    @property
    @pulumi.getter
    def attachments(self) -> Sequence['outputs.GetTransitRouterVbrAttachmentsAttachmentResult']:
        """
        A list of CEN Transit Router VBR Attachments. Each element contains the following attributes:
        """
        return pulumi.get(self, "attachments")

    @property
    @pulumi.getter(name="cenId")
    def cen_id(self) -> str:
        return pulumi.get(self, "cen_id")

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
        A list of CEN Transit Router VBR attachment IDs.
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
        The status of the transit router attachment.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="transitRouterId")
    def transit_router_id(self) -> Optional[str]:
        return pulumi.get(self, "transit_router_id")


class AwaitableGetTransitRouterVbrAttachmentsResult(GetTransitRouterVbrAttachmentsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTransitRouterVbrAttachmentsResult(
            attachments=self.attachments,
            cen_id=self.cen_id,
            id=self.id,
            ids=self.ids,
            output_file=self.output_file,
            status=self.status,
            transit_router_id=self.transit_router_id)


def get_transit_router_vbr_attachments(cen_id: Optional[str] = None,
                                       ids: Optional[Sequence[str]] = None,
                                       output_file: Optional[str] = None,
                                       status: Optional[str] = None,
                                       transit_router_id: Optional[str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTransitRouterVbrAttachmentsResult:
    """
    This data source provides CEN Transit Router VBR Attachments available to the user.[What is Cen Transit Router VBR Attachments](https://help.aliyun.com/document_detail/261226.html)

    > **NOTE:** Available in 1.126.0+


    :param str cen_id: ID of the CEN instance.
    :param Sequence[str] ids: A list of resource id. The element value is same as `transit_router_id`.
    :param str status: The status of the resource. Valid values `Attached`, `Attaching` and `Detaching`.
    :param str transit_router_id: ID of the transit router.
    """
    __args__ = dict()
    __args__['cenId'] = cen_id
    __args__['ids'] = ids
    __args__['outputFile'] = output_file
    __args__['status'] = status
    __args__['transitRouterId'] = transit_router_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:cen/getTransitRouterVbrAttachments:getTransitRouterVbrAttachments', __args__, opts=opts, typ=GetTransitRouterVbrAttachmentsResult).value

    return AwaitableGetTransitRouterVbrAttachmentsResult(
        attachments=__ret__.attachments,
        cen_id=__ret__.cen_id,
        id=__ret__.id,
        ids=__ret__.ids,
        output_file=__ret__.output_file,
        status=__ret__.status,
        transit_router_id=__ret__.transit_router_id)


@_utilities.lift_output_func(get_transit_router_vbr_attachments)
def get_transit_router_vbr_attachments_output(cen_id: Optional[pulumi.Input[str]] = None,
                                              ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                              output_file: Optional[pulumi.Input[Optional[str]]] = None,
                                              status: Optional[pulumi.Input[Optional[str]]] = None,
                                              transit_router_id: Optional[pulumi.Input[Optional[str]]] = None,
                                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTransitRouterVbrAttachmentsResult]:
    """
    This data source provides CEN Transit Router VBR Attachments available to the user.[What is Cen Transit Router VBR Attachments](https://help.aliyun.com/document_detail/261226.html)

    > **NOTE:** Available in 1.126.0+


    :param str cen_id: ID of the CEN instance.
    :param Sequence[str] ids: A list of resource id. The element value is same as `transit_router_id`.
    :param str status: The status of the resource. Valid values `Attached`, `Attaching` and `Detaching`.
    :param str transit_router_id: ID of the transit router.
    """
    ...
