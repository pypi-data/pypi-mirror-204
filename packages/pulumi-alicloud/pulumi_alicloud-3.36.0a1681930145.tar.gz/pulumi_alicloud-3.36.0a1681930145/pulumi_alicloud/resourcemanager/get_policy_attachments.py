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
    'GetPolicyAttachmentsResult',
    'AwaitableGetPolicyAttachmentsResult',
    'get_policy_attachments',
    'get_policy_attachments_output',
]

@pulumi.output_type
class GetPolicyAttachmentsResult:
    """
    A collection of values returned by getPolicyAttachments.
    """
    def __init__(__self__, attachments=None, id=None, ids=None, language=None, output_file=None, policy_name=None, policy_type=None, principal_name=None, principal_type=None, resource_group_id=None):
        if attachments and not isinstance(attachments, list):
            raise TypeError("Expected argument 'attachments' to be a list")
        pulumi.set(__self__, "attachments", attachments)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if language and not isinstance(language, str):
            raise TypeError("Expected argument 'language' to be a str")
        pulumi.set(__self__, "language", language)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if policy_name and not isinstance(policy_name, str):
            raise TypeError("Expected argument 'policy_name' to be a str")
        pulumi.set(__self__, "policy_name", policy_name)
        if policy_type and not isinstance(policy_type, str):
            raise TypeError("Expected argument 'policy_type' to be a str")
        pulumi.set(__self__, "policy_type", policy_type)
        if principal_name and not isinstance(principal_name, str):
            raise TypeError("Expected argument 'principal_name' to be a str")
        pulumi.set(__self__, "principal_name", principal_name)
        if principal_type and not isinstance(principal_type, str):
            raise TypeError("Expected argument 'principal_type' to be a str")
        pulumi.set(__self__, "principal_type", principal_type)
        if resource_group_id and not isinstance(resource_group_id, str):
            raise TypeError("Expected argument 'resource_group_id' to be a str")
        pulumi.set(__self__, "resource_group_id", resource_group_id)

    @property
    @pulumi.getter
    def attachments(self) -> Sequence['outputs.GetPolicyAttachmentsAttachmentResult']:
        """
        A list of Resource Manager Policy Attachment. Each element contains the following attributes:
        """
        return pulumi.get(self, "attachments")

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
        A list of Resource Manager Policy Attachment IDs.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter
    def language(self) -> Optional[str]:
        return pulumi.get(self, "language")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> Optional[str]:
        """
        The name of the policy.
        """
        return pulumi.get(self, "policy_name")

    @property
    @pulumi.getter(name="policyType")
    def policy_type(self) -> Optional[str]:
        """
        The type of the policy.
        """
        return pulumi.get(self, "policy_type")

    @property
    @pulumi.getter(name="principalName")
    def principal_name(self) -> Optional[str]:
        """
        The name of the object to which the policy is attached.
        """
        return pulumi.get(self, "principal_name")

    @property
    @pulumi.getter(name="principalType")
    def principal_type(self) -> Optional[str]:
        """
        The type of the object to which the policy is attached.
        """
        return pulumi.get(self, "principal_type")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[str]:
        """
        The ID of the resource group or the ID of the Alibaba Cloud account to which the resource group belongs.
        """
        return pulumi.get(self, "resource_group_id")


class AwaitableGetPolicyAttachmentsResult(GetPolicyAttachmentsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicyAttachmentsResult(
            attachments=self.attachments,
            id=self.id,
            ids=self.ids,
            language=self.language,
            output_file=self.output_file,
            policy_name=self.policy_name,
            policy_type=self.policy_type,
            principal_name=self.principal_name,
            principal_type=self.principal_type,
            resource_group_id=self.resource_group_id)


def get_policy_attachments(language: Optional[str] = None,
                           output_file: Optional[str] = None,
                           policy_name: Optional[str] = None,
                           policy_type: Optional[str] = None,
                           principal_name: Optional[str] = None,
                           principal_type: Optional[str] = None,
                           resource_group_id: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicyAttachmentsResult:
    """
    This data source provides the Resource Manager Policy Attachments of the current Alibaba Cloud user.

    > **NOTE:**  Available in 1.93.0+.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.resourcemanager.get_policy_attachments()
    pulumi.export("firstAttachmentId", example.attachments[0].id)
    ```


    :param str language: The language that is used to return the description of the system policy. Valid values:`en`: English, `zh-CN`: Chinese, `ja`: Japanese.
    :param str policy_name: The name of the policy. The name must be 1 to 128 characters in length and can contain letters, digits, and hyphens (-).
    :param str policy_type: The type of the policy. Valid values: `Custom` and `System`.
    :param str principal_name: The name of the object to which the policy is attached.
    :param str principal_type: The type of the object to which the policy is attached. If you do not specify this parameter, the system lists all types of objects. Valid values: `IMSUser`: RAM user, `IMSGroup`: RAM user group, `ServiceRole`: RAM role.
    :param str resource_group_id: The ID of the resource group or the ID of the Alibaba Cloud account to which the resource group belongs. If you do not specify this parameter, the system lists all policy attachment records under the current account.
    """
    __args__ = dict()
    __args__['language'] = language
    __args__['outputFile'] = output_file
    __args__['policyName'] = policy_name
    __args__['policyType'] = policy_type
    __args__['principalName'] = principal_name
    __args__['principalType'] = principal_type
    __args__['resourceGroupId'] = resource_group_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:resourcemanager/getPolicyAttachments:getPolicyAttachments', __args__, opts=opts, typ=GetPolicyAttachmentsResult).value

    return AwaitableGetPolicyAttachmentsResult(
        attachments=__ret__.attachments,
        id=__ret__.id,
        ids=__ret__.ids,
        language=__ret__.language,
        output_file=__ret__.output_file,
        policy_name=__ret__.policy_name,
        policy_type=__ret__.policy_type,
        principal_name=__ret__.principal_name,
        principal_type=__ret__.principal_type,
        resource_group_id=__ret__.resource_group_id)


@_utilities.lift_output_func(get_policy_attachments)
def get_policy_attachments_output(language: Optional[pulumi.Input[Optional[str]]] = None,
                                  output_file: Optional[pulumi.Input[Optional[str]]] = None,
                                  policy_name: Optional[pulumi.Input[Optional[str]]] = None,
                                  policy_type: Optional[pulumi.Input[Optional[str]]] = None,
                                  principal_name: Optional[pulumi.Input[Optional[str]]] = None,
                                  principal_type: Optional[pulumi.Input[Optional[str]]] = None,
                                  resource_group_id: Optional[pulumi.Input[Optional[str]]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPolicyAttachmentsResult]:
    """
    This data source provides the Resource Manager Policy Attachments of the current Alibaba Cloud user.

    > **NOTE:**  Available in 1.93.0+.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.resourcemanager.get_policy_attachments()
    pulumi.export("firstAttachmentId", example.attachments[0].id)
    ```


    :param str language: The language that is used to return the description of the system policy. Valid values:`en`: English, `zh-CN`: Chinese, `ja`: Japanese.
    :param str policy_name: The name of the policy. The name must be 1 to 128 characters in length and can contain letters, digits, and hyphens (-).
    :param str policy_type: The type of the policy. Valid values: `Custom` and `System`.
    :param str principal_name: The name of the object to which the policy is attached.
    :param str principal_type: The type of the object to which the policy is attached. If you do not specify this parameter, the system lists all types of objects. Valid values: `IMSUser`: RAM user, `IMSGroup`: RAM user group, `ServiceRole`: RAM role.
    :param str resource_group_id: The ID of the resource group or the ID of the Alibaba Cloud account to which the resource group belongs. If you do not specify this parameter, the system lists all policy attachment records under the current account.
    """
    ...
