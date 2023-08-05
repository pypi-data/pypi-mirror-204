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
    'GetJobTemplatesResult',
    'AwaitableGetJobTemplatesResult',
    'get_job_templates',
    'get_job_templates_output',
]

@pulumi.output_type
class GetJobTemplatesResult:
    """
    A collection of values returned by getJobTemplates.
    """
    def __init__(__self__, id=None, ids=None, output_file=None, templates=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if templates and not isinstance(templates, list):
            raise TypeError("Expected argument 'templates' to be a list")
        pulumi.set(__self__, "templates", templates)

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
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def templates(self) -> Sequence['outputs.GetJobTemplatesTemplateResult']:
        return pulumi.get(self, "templates")


class AwaitableGetJobTemplatesResult(GetJobTemplatesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetJobTemplatesResult(
            id=self.id,
            ids=self.ids,
            output_file=self.output_file,
            templates=self.templates)


def get_job_templates(ids: Optional[Sequence[str]] = None,
                      output_file: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetJobTemplatesResult:
    """
    This data source provides the Ehpc Job Templates of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.133.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.ehpc.JobTemplate("default",
        job_template_name="example_value",
        command_line="./LammpsTest/lammps.pbs")
    ids = alicloud.ehpc.get_job_templates_output(ids=[default.id])
    pulumi.export("ehpcJobTemplateId1", ids.id)
    ```


    :param Sequence[str] ids: A list of Job Template IDs.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['outputFile'] = output_file
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:ehpc/getJobTemplates:getJobTemplates', __args__, opts=opts, typ=GetJobTemplatesResult).value

    return AwaitableGetJobTemplatesResult(
        id=__ret__.id,
        ids=__ret__.ids,
        output_file=__ret__.output_file,
        templates=__ret__.templates)


@_utilities.lift_output_func(get_job_templates)
def get_job_templates_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                             output_file: Optional[pulumi.Input[Optional[str]]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetJobTemplatesResult]:
    """
    This data source provides the Ehpc Job Templates of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.133.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.ehpc.JobTemplate("default",
        job_template_name="example_value",
        command_line="./LammpsTest/lammps.pbs")
    ids = alicloud.ehpc.get_job_templates_output(ids=[default.id])
    pulumi.export("ehpcJobTemplateId1", ids.id)
    ```


    :param Sequence[str] ids: A list of Job Template IDs.
    """
    ...
