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
    'GetAscriptsResult',
    'AwaitableGetAscriptsResult',
    'get_ascripts',
    'get_ascripts_output',
]

@pulumi.output_type
class GetAscriptsResult:
    """
    A collection of values returned by getAscripts.
    """
    def __init__(__self__, ascript_name=None, ascripts=None, enable_details=None, id=None, ids=None, listener_id=None, name_regex=None, names=None, output_file=None):
        if ascript_name and not isinstance(ascript_name, str):
            raise TypeError("Expected argument 'ascript_name' to be a str")
        pulumi.set(__self__, "ascript_name", ascript_name)
        if ascripts and not isinstance(ascripts, list):
            raise TypeError("Expected argument 'ascripts' to be a list")
        pulumi.set(__self__, "ascripts", ascripts)
        if enable_details and not isinstance(enable_details, bool):
            raise TypeError("Expected argument 'enable_details' to be a bool")
        pulumi.set(__self__, "enable_details", enable_details)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if listener_id and not isinstance(listener_id, str):
            raise TypeError("Expected argument 'listener_id' to be a str")
        pulumi.set(__self__, "listener_id", listener_id)
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
    @pulumi.getter(name="ascriptName")
    def ascript_name(self) -> Optional[str]:
        """
        Script name.
        """
        return pulumi.get(self, "ascript_name")

    @property
    @pulumi.getter
    def ascripts(self) -> Sequence['outputs.GetAscriptsAscriptResult']:
        """
        A list of AScript Entries. Each element contains the following attributes:
        """
        return pulumi.get(self, "ascripts")

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
        """
        A list of AScript IDs.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> Optional[str]:
        """
        Listener ID of script attribution.
        """
        return pulumi.get(self, "listener_id")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        """
        A list of name of AScripts.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")


class AwaitableGetAscriptsResult(GetAscriptsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAscriptsResult(
            ascript_name=self.ascript_name,
            ascripts=self.ascripts,
            enable_details=self.enable_details,
            id=self.id,
            ids=self.ids,
            listener_id=self.listener_id,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file)


def get_ascripts(ascript_name: Optional[str] = None,
                 enable_details: Optional[bool] = None,
                 ids: Optional[Sequence[str]] = None,
                 listener_id: Optional[str] = None,
                 name_regex: Optional[str] = None,
                 output_file: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAscriptsResult:
    """
    This data source provides Alb Ascript available to the user.

    > **NOTE:** Available in 1.195.0+

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.alb.get_ascripts(ids=[alicloud_alb_ascript["default"]["id"]],
        name_regex=alicloud_alb_ascript["default"]["name"],
        ascript_name="test",
        listener_id=var["listenerId"])
    pulumi.export("alicloudAlbAscriptExampleId", default.ascripts[0].id)
    ```


    :param str ascript_name: Script name.
    :param Sequence[str] ids: A list of AScript IDs.
    :param str listener_id: Listener ID of script attribution
    :param str name_regex: A regex string to filter results by Group Metric Rule name.
    """
    __args__ = dict()
    __args__['ascriptName'] = ascript_name
    __args__['enableDetails'] = enable_details
    __args__['ids'] = ids
    __args__['listenerId'] = listener_id
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:alb/getAscripts:getAscripts', __args__, opts=opts, typ=GetAscriptsResult).value

    return AwaitableGetAscriptsResult(
        ascript_name=__ret__.ascript_name,
        ascripts=__ret__.ascripts,
        enable_details=__ret__.enable_details,
        id=__ret__.id,
        ids=__ret__.ids,
        listener_id=__ret__.listener_id,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file)


@_utilities.lift_output_func(get_ascripts)
def get_ascripts_output(ascript_name: Optional[pulumi.Input[Optional[str]]] = None,
                        enable_details: Optional[pulumi.Input[Optional[bool]]] = None,
                        ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                        listener_id: Optional[pulumi.Input[Optional[str]]] = None,
                        name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                        output_file: Optional[pulumi.Input[Optional[str]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAscriptsResult]:
    """
    This data source provides Alb Ascript available to the user.

    > **NOTE:** Available in 1.195.0+

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.alb.get_ascripts(ids=[alicloud_alb_ascript["default"]["id"]],
        name_regex=alicloud_alb_ascript["default"]["name"],
        ascript_name="test",
        listener_id=var["listenerId"])
    pulumi.export("alicloudAlbAscriptExampleId", default.ascripts[0].id)
    ```


    :param str ascript_name: Script name.
    :param Sequence[str] ids: A list of AScript IDs.
    :param str listener_id: Listener ID of script attribution
    :param str name_regex: A regex string to filter results by Group Metric Rule name.
    """
    ...
