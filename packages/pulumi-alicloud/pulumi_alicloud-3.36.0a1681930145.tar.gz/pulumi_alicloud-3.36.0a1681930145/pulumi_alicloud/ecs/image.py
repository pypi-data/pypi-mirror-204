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
from ._inputs import *

__all__ = ['ImageArgs', 'Image']

@pulumi.input_type
class ImageArgs:
    def __init__(__self__, *,
                 architecture: Optional[pulumi.Input[str]] = None,
                 delete_auto_snapshot: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 disk_device_mappings: Optional[pulumi.Input[Sequence[pulumi.Input['ImageDiskDeviceMappingArgs']]]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 image_name: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 snapshot_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None):
        """
        The set of arguments for constructing a Image resource.
        :param pulumi.Input[str] architecture: Specifies the architecture of the system disk after you specify a data disk snapshot as the data source of the system disk for creating an image. Valid values: `i386` , Default is `x86_64`.
        :param pulumi.Input[str] description: The description of the image. It must be 2 to 256 characters in length and must not start with http:// or https://. Default value: null.
        :param pulumi.Input[Sequence[pulumi.Input['ImageDiskDeviceMappingArgs']]] disk_device_mappings: Description of the system with disks and snapshots under the image.
        :param pulumi.Input[bool] force: Indicates whether to force delete the custom image, Default is `false`. 
               - true：Force deletes the custom image, regardless of whether the image is currently being used by other instances.
               - false：Verifies that the image is not currently in use by any other instances before deleting the image.
        :param pulumi.Input[str] image_name: The image name. It must be 2 to 128 characters in length, and must begin with a letter or Chinese character (beginning with http:// or https:// is not allowed). It can contain digits, colons (:), underscores (_), or hyphens (-). Default value: null.
        :param pulumi.Input[str] instance_id: The instance ID.
        :param pulumi.Input[str] platform: The distribution of the operating system for the system disk in the custom image. 
               If you specify a data disk snapshot to create the system disk of the custom image, you must use the Platform parameter
               to specify the distribution of the operating system for the system disk. Default value: Others Linux.
               More valid values refer to [CreateImage OpenAPI](https://www.alibabacloud.com/help/en/elastic-compute-service/latest/createimage)
               **NOTE**: It's default value is Ubuntu before version 1.197.0.
        :param pulumi.Input[str] resource_group_id: The ID of the enterprise resource group to which a custom image belongs
        :param pulumi.Input[str] snapshot_id: Specifies a snapshot that is used to create a combined custom image.
        :param pulumi.Input[Mapping[str, Any]] tags: The tag value of an image. The value of N ranges from 1 to 20.
        """
        if architecture is not None:
            pulumi.set(__self__, "architecture", architecture)
        if delete_auto_snapshot is not None:
            pulumi.set(__self__, "delete_auto_snapshot", delete_auto_snapshot)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if disk_device_mappings is not None:
            pulumi.set(__self__, "disk_device_mappings", disk_device_mappings)
        if force is not None:
            pulumi.set(__self__, "force", force)
        if image_name is not None:
            pulumi.set(__self__, "image_name", image_name)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if name is not None:
            warnings.warn("""Attribute 'name' has been deprecated from version 1.69.0. Use `image_name` instead.""", DeprecationWarning)
            pulumi.log.warn("""name is deprecated: Attribute 'name' has been deprecated from version 1.69.0. Use `image_name` instead.""")
        if name is not None:
            pulumi.set(__self__, "name", name)
        if platform is not None:
            pulumi.set(__self__, "platform", platform)
        if resource_group_id is not None:
            pulumi.set(__self__, "resource_group_id", resource_group_id)
        if snapshot_id is not None:
            pulumi.set(__self__, "snapshot_id", snapshot_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def architecture(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the architecture of the system disk after you specify a data disk snapshot as the data source of the system disk for creating an image. Valid values: `i386` , Default is `x86_64`.
        """
        return pulumi.get(self, "architecture")

    @architecture.setter
    def architecture(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "architecture", value)

    @property
    @pulumi.getter(name="deleteAutoSnapshot")
    def delete_auto_snapshot(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "delete_auto_snapshot")

    @delete_auto_snapshot.setter
    def delete_auto_snapshot(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delete_auto_snapshot", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the image. It must be 2 to 256 characters in length and must not start with http:// or https://. Default value: null.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="diskDeviceMappings")
    def disk_device_mappings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ImageDiskDeviceMappingArgs']]]]:
        """
        Description of the system with disks and snapshots under the image.
        """
        return pulumi.get(self, "disk_device_mappings")

    @disk_device_mappings.setter
    def disk_device_mappings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ImageDiskDeviceMappingArgs']]]]):
        pulumi.set(self, "disk_device_mappings", value)

    @property
    @pulumi.getter
    def force(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether to force delete the custom image, Default is `false`. 
        - true：Force deletes the custom image, regardless of whether the image is currently being used by other instances.
        - false：Verifies that the image is not currently in use by any other instances before deleting the image.
        """
        return pulumi.get(self, "force")

    @force.setter
    def force(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force", value)

    @property
    @pulumi.getter(name="imageName")
    def image_name(self) -> Optional[pulumi.Input[str]]:
        """
        The image name. It must be 2 to 128 characters in length, and must begin with a letter or Chinese character (beginning with http:// or https:// is not allowed). It can contain digits, colons (:), underscores (_), or hyphens (-). Default value: null.
        """
        return pulumi.get(self, "image_name")

    @image_name.setter
    def image_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "image_name", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The instance ID.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def platform(self) -> Optional[pulumi.Input[str]]:
        """
        The distribution of the operating system for the system disk in the custom image. 
        If you specify a data disk snapshot to create the system disk of the custom image, you must use the Platform parameter
        to specify the distribution of the operating system for the system disk. Default value: Others Linux.
        More valid values refer to [CreateImage OpenAPI](https://www.alibabacloud.com/help/en/elastic-compute-service/latest/createimage)
        **NOTE**: It's default value is Ubuntu before version 1.197.0.
        """
        return pulumi.get(self, "platform")

    @platform.setter
    def platform(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "platform", value)

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the enterprise resource group to which a custom image belongs
        """
        return pulumi.get(self, "resource_group_id")

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_id", value)

    @property
    @pulumi.getter(name="snapshotId")
    def snapshot_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a snapshot that is used to create a combined custom image.
        """
        return pulumi.get(self, "snapshot_id")

    @snapshot_id.setter
    def snapshot_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "snapshot_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        The tag value of an image. The value of N ranges from 1 to 20.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ImageState:
    def __init__(__self__, *,
                 architecture: Optional[pulumi.Input[str]] = None,
                 delete_auto_snapshot: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 disk_device_mappings: Optional[pulumi.Input[Sequence[pulumi.Input['ImageDiskDeviceMappingArgs']]]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 image_name: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 snapshot_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None):
        """
        Input properties used for looking up and filtering Image resources.
        :param pulumi.Input[str] architecture: Specifies the architecture of the system disk after you specify a data disk snapshot as the data source of the system disk for creating an image. Valid values: `i386` , Default is `x86_64`.
        :param pulumi.Input[str] description: The description of the image. It must be 2 to 256 characters in length and must not start with http:// or https://. Default value: null.
        :param pulumi.Input[Sequence[pulumi.Input['ImageDiskDeviceMappingArgs']]] disk_device_mappings: Description of the system with disks and snapshots under the image.
        :param pulumi.Input[bool] force: Indicates whether to force delete the custom image, Default is `false`. 
               - true：Force deletes the custom image, regardless of whether the image is currently being used by other instances.
               - false：Verifies that the image is not currently in use by any other instances before deleting the image.
        :param pulumi.Input[str] image_name: The image name. It must be 2 to 128 characters in length, and must begin with a letter or Chinese character (beginning with http:// or https:// is not allowed). It can contain digits, colons (:), underscores (_), or hyphens (-). Default value: null.
        :param pulumi.Input[str] instance_id: The instance ID.
        :param pulumi.Input[str] platform: The distribution of the operating system for the system disk in the custom image. 
               If you specify a data disk snapshot to create the system disk of the custom image, you must use the Platform parameter
               to specify the distribution of the operating system for the system disk. Default value: Others Linux.
               More valid values refer to [CreateImage OpenAPI](https://www.alibabacloud.com/help/en/elastic-compute-service/latest/createimage)
               **NOTE**: It's default value is Ubuntu before version 1.197.0.
        :param pulumi.Input[str] resource_group_id: The ID of the enterprise resource group to which a custom image belongs
        :param pulumi.Input[str] snapshot_id: Specifies a snapshot that is used to create a combined custom image.
        :param pulumi.Input[Mapping[str, Any]] tags: The tag value of an image. The value of N ranges from 1 to 20.
        """
        if architecture is not None:
            pulumi.set(__self__, "architecture", architecture)
        if delete_auto_snapshot is not None:
            pulumi.set(__self__, "delete_auto_snapshot", delete_auto_snapshot)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if disk_device_mappings is not None:
            pulumi.set(__self__, "disk_device_mappings", disk_device_mappings)
        if force is not None:
            pulumi.set(__self__, "force", force)
        if image_name is not None:
            pulumi.set(__self__, "image_name", image_name)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if name is not None:
            warnings.warn("""Attribute 'name' has been deprecated from version 1.69.0. Use `image_name` instead.""", DeprecationWarning)
            pulumi.log.warn("""name is deprecated: Attribute 'name' has been deprecated from version 1.69.0. Use `image_name` instead.""")
        if name is not None:
            pulumi.set(__self__, "name", name)
        if platform is not None:
            pulumi.set(__self__, "platform", platform)
        if resource_group_id is not None:
            pulumi.set(__self__, "resource_group_id", resource_group_id)
        if snapshot_id is not None:
            pulumi.set(__self__, "snapshot_id", snapshot_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def architecture(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the architecture of the system disk after you specify a data disk snapshot as the data source of the system disk for creating an image. Valid values: `i386` , Default is `x86_64`.
        """
        return pulumi.get(self, "architecture")

    @architecture.setter
    def architecture(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "architecture", value)

    @property
    @pulumi.getter(name="deleteAutoSnapshot")
    def delete_auto_snapshot(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "delete_auto_snapshot")

    @delete_auto_snapshot.setter
    def delete_auto_snapshot(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delete_auto_snapshot", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the image. It must be 2 to 256 characters in length and must not start with http:// or https://. Default value: null.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="diskDeviceMappings")
    def disk_device_mappings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ImageDiskDeviceMappingArgs']]]]:
        """
        Description of the system with disks and snapshots under the image.
        """
        return pulumi.get(self, "disk_device_mappings")

    @disk_device_mappings.setter
    def disk_device_mappings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ImageDiskDeviceMappingArgs']]]]):
        pulumi.set(self, "disk_device_mappings", value)

    @property
    @pulumi.getter
    def force(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether to force delete the custom image, Default is `false`. 
        - true：Force deletes the custom image, regardless of whether the image is currently being used by other instances.
        - false：Verifies that the image is not currently in use by any other instances before deleting the image.
        """
        return pulumi.get(self, "force")

    @force.setter
    def force(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force", value)

    @property
    @pulumi.getter(name="imageName")
    def image_name(self) -> Optional[pulumi.Input[str]]:
        """
        The image name. It must be 2 to 128 characters in length, and must begin with a letter or Chinese character (beginning with http:// or https:// is not allowed). It can contain digits, colons (:), underscores (_), or hyphens (-). Default value: null.
        """
        return pulumi.get(self, "image_name")

    @image_name.setter
    def image_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "image_name", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The instance ID.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def platform(self) -> Optional[pulumi.Input[str]]:
        """
        The distribution of the operating system for the system disk in the custom image. 
        If you specify a data disk snapshot to create the system disk of the custom image, you must use the Platform parameter
        to specify the distribution of the operating system for the system disk. Default value: Others Linux.
        More valid values refer to [CreateImage OpenAPI](https://www.alibabacloud.com/help/en/elastic-compute-service/latest/createimage)
        **NOTE**: It's default value is Ubuntu before version 1.197.0.
        """
        return pulumi.get(self, "platform")

    @platform.setter
    def platform(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "platform", value)

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the enterprise resource group to which a custom image belongs
        """
        return pulumi.get(self, "resource_group_id")

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_id", value)

    @property
    @pulumi.getter(name="snapshotId")
    def snapshot_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a snapshot that is used to create a combined custom image.
        """
        return pulumi.get(self, "snapshot_id")

    @snapshot_id.setter
    def snapshot_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "snapshot_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        The tag value of an image. The value of N ranges from 1 to 20.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "tags", value)


class Image(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 architecture: Optional[pulumi.Input[str]] = None,
                 delete_auto_snapshot: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 disk_device_mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageDiskDeviceMappingArgs']]]]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 image_name: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 snapshot_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 __props__=None):
        """
        Creates a custom image. You can then use a custom image to create ECS instances (RunInstances) or change the system disk for an existing instance (ReplaceSystemDisk).

        > **NOTE:**  If you want to create a template from an ECS instance, you can specify the instance ID (InstanceId) to create a custom image. You must make sure that the status of the specified instance is Running or Stopped. After a successful invocation, each disk of the specified instance has a new snapshot created.

        > **NOTE:**  If you want to create a custom image based on the system disk of your ECS instance, you can specify one of the system disk snapshots (SnapshotId) to create a custom image. However, the specified snapshot cannot be created on or before July 15, 2013.

        > **NOTE:**  If you want to combine snapshots of multiple disks into an image template, you can specify DiskDeviceMapping to create a custom image.

        > **NOTE:**  Available in 1.64.0+

        ## Example Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.ecs.Image("default",
            architecture="x86_64",
            description="test-image",
            image_name="test-image",
            instance_id="i-bp1g6zv0ce8oghu7k***",
            platform="CentOS",
            resource_group_id="rg-bp67acfmxazb4ph***",
            tags={
                "FinanceDept": "FinanceDeptJoshua",
            })
        ```

        ## Import

         image can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:ecs/image:Image default m-uf66871ape***yg1q***
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] architecture: Specifies the architecture of the system disk after you specify a data disk snapshot as the data source of the system disk for creating an image. Valid values: `i386` , Default is `x86_64`.
        :param pulumi.Input[str] description: The description of the image. It must be 2 to 256 characters in length and must not start with http:// or https://. Default value: null.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageDiskDeviceMappingArgs']]]] disk_device_mappings: Description of the system with disks and snapshots under the image.
        :param pulumi.Input[bool] force: Indicates whether to force delete the custom image, Default is `false`. 
               - true：Force deletes the custom image, regardless of whether the image is currently being used by other instances.
               - false：Verifies that the image is not currently in use by any other instances before deleting the image.
        :param pulumi.Input[str] image_name: The image name. It must be 2 to 128 characters in length, and must begin with a letter or Chinese character (beginning with http:// or https:// is not allowed). It can contain digits, colons (:), underscores (_), or hyphens (-). Default value: null.
        :param pulumi.Input[str] instance_id: The instance ID.
        :param pulumi.Input[str] platform: The distribution of the operating system for the system disk in the custom image. 
               If you specify a data disk snapshot to create the system disk of the custom image, you must use the Platform parameter
               to specify the distribution of the operating system for the system disk. Default value: Others Linux.
               More valid values refer to [CreateImage OpenAPI](https://www.alibabacloud.com/help/en/elastic-compute-service/latest/createimage)
               **NOTE**: It's default value is Ubuntu before version 1.197.0.
        :param pulumi.Input[str] resource_group_id: The ID of the enterprise resource group to which a custom image belongs
        :param pulumi.Input[str] snapshot_id: Specifies a snapshot that is used to create a combined custom image.
        :param pulumi.Input[Mapping[str, Any]] tags: The tag value of an image. The value of N ranges from 1 to 20.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ImageArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a custom image. You can then use a custom image to create ECS instances (RunInstances) or change the system disk for an existing instance (ReplaceSystemDisk).

        > **NOTE:**  If you want to create a template from an ECS instance, you can specify the instance ID (InstanceId) to create a custom image. You must make sure that the status of the specified instance is Running or Stopped. After a successful invocation, each disk of the specified instance has a new snapshot created.

        > **NOTE:**  If you want to create a custom image based on the system disk of your ECS instance, you can specify one of the system disk snapshots (SnapshotId) to create a custom image. However, the specified snapshot cannot be created on or before July 15, 2013.

        > **NOTE:**  If you want to combine snapshots of multiple disks into an image template, you can specify DiskDeviceMapping to create a custom image.

        > **NOTE:**  Available in 1.64.0+

        ## Example Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.ecs.Image("default",
            architecture="x86_64",
            description="test-image",
            image_name="test-image",
            instance_id="i-bp1g6zv0ce8oghu7k***",
            platform="CentOS",
            resource_group_id="rg-bp67acfmxazb4ph***",
            tags={
                "FinanceDept": "FinanceDeptJoshua",
            })
        ```

        ## Import

         image can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:ecs/image:Image default m-uf66871ape***yg1q***
        ```

        :param str resource_name: The name of the resource.
        :param ImageArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ImageArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 architecture: Optional[pulumi.Input[str]] = None,
                 delete_auto_snapshot: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 disk_device_mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageDiskDeviceMappingArgs']]]]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 image_name: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 snapshot_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ImageArgs.__new__(ImageArgs)

            __props__.__dict__["architecture"] = architecture
            __props__.__dict__["delete_auto_snapshot"] = delete_auto_snapshot
            __props__.__dict__["description"] = description
            __props__.__dict__["disk_device_mappings"] = disk_device_mappings
            __props__.__dict__["force"] = force
            __props__.__dict__["image_name"] = image_name
            __props__.__dict__["instance_id"] = instance_id
            if name is not None and not opts.urn:
                warnings.warn("""Attribute 'name' has been deprecated from version 1.69.0. Use `image_name` instead.""", DeprecationWarning)
                pulumi.log.warn("""name is deprecated: Attribute 'name' has been deprecated from version 1.69.0. Use `image_name` instead.""")
            __props__.__dict__["name"] = name
            __props__.__dict__["platform"] = platform
            __props__.__dict__["resource_group_id"] = resource_group_id
            __props__.__dict__["snapshot_id"] = snapshot_id
            __props__.__dict__["tags"] = tags
        super(Image, __self__).__init__(
            'alicloud:ecs/image:Image',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            architecture: Optional[pulumi.Input[str]] = None,
            delete_auto_snapshot: Optional[pulumi.Input[bool]] = None,
            description: Optional[pulumi.Input[str]] = None,
            disk_device_mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageDiskDeviceMappingArgs']]]]] = None,
            force: Optional[pulumi.Input[bool]] = None,
            image_name: Optional[pulumi.Input[str]] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            platform: Optional[pulumi.Input[str]] = None,
            resource_group_id: Optional[pulumi.Input[str]] = None,
            snapshot_id: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, Any]]] = None) -> 'Image':
        """
        Get an existing Image resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] architecture: Specifies the architecture of the system disk after you specify a data disk snapshot as the data source of the system disk for creating an image. Valid values: `i386` , Default is `x86_64`.
        :param pulumi.Input[str] description: The description of the image. It must be 2 to 256 characters in length and must not start with http:// or https://. Default value: null.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageDiskDeviceMappingArgs']]]] disk_device_mappings: Description of the system with disks and snapshots under the image.
        :param pulumi.Input[bool] force: Indicates whether to force delete the custom image, Default is `false`. 
               - true：Force deletes the custom image, regardless of whether the image is currently being used by other instances.
               - false：Verifies that the image is not currently in use by any other instances before deleting the image.
        :param pulumi.Input[str] image_name: The image name. It must be 2 to 128 characters in length, and must begin with a letter or Chinese character (beginning with http:// or https:// is not allowed). It can contain digits, colons (:), underscores (_), or hyphens (-). Default value: null.
        :param pulumi.Input[str] instance_id: The instance ID.
        :param pulumi.Input[str] platform: The distribution of the operating system for the system disk in the custom image. 
               If you specify a data disk snapshot to create the system disk of the custom image, you must use the Platform parameter
               to specify the distribution of the operating system for the system disk. Default value: Others Linux.
               More valid values refer to [CreateImage OpenAPI](https://www.alibabacloud.com/help/en/elastic-compute-service/latest/createimage)
               **NOTE**: It's default value is Ubuntu before version 1.197.0.
        :param pulumi.Input[str] resource_group_id: The ID of the enterprise resource group to which a custom image belongs
        :param pulumi.Input[str] snapshot_id: Specifies a snapshot that is used to create a combined custom image.
        :param pulumi.Input[Mapping[str, Any]] tags: The tag value of an image. The value of N ranges from 1 to 20.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ImageState.__new__(_ImageState)

        __props__.__dict__["architecture"] = architecture
        __props__.__dict__["delete_auto_snapshot"] = delete_auto_snapshot
        __props__.__dict__["description"] = description
        __props__.__dict__["disk_device_mappings"] = disk_device_mappings
        __props__.__dict__["force"] = force
        __props__.__dict__["image_name"] = image_name
        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["name"] = name
        __props__.__dict__["platform"] = platform
        __props__.__dict__["resource_group_id"] = resource_group_id
        __props__.__dict__["snapshot_id"] = snapshot_id
        __props__.__dict__["tags"] = tags
        return Image(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def architecture(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the architecture of the system disk after you specify a data disk snapshot as the data source of the system disk for creating an image. Valid values: `i386` , Default is `x86_64`.
        """
        return pulumi.get(self, "architecture")

    @property
    @pulumi.getter(name="deleteAutoSnapshot")
    def delete_auto_snapshot(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "delete_auto_snapshot")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the image. It must be 2 to 256 characters in length and must not start with http:// or https://. Default value: null.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="diskDeviceMappings")
    def disk_device_mappings(self) -> pulumi.Output[Sequence['outputs.ImageDiskDeviceMapping']]:
        """
        Description of the system with disks and snapshots under the image.
        """
        return pulumi.get(self, "disk_device_mappings")

    @property
    @pulumi.getter
    def force(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether to force delete the custom image, Default is `false`. 
        - true：Force deletes the custom image, regardless of whether the image is currently being used by other instances.
        - false：Verifies that the image is not currently in use by any other instances before deleting the image.
        """
        return pulumi.get(self, "force")

    @property
    @pulumi.getter(name="imageName")
    def image_name(self) -> pulumi.Output[str]:
        """
        The image name. It must be 2 to 128 characters in length, and must begin with a letter or Chinese character (beginning with http:// or https:// is not allowed). It can contain digits, colons (:), underscores (_), or hyphens (-). Default value: null.
        """
        return pulumi.get(self, "image_name")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[Optional[str]]:
        """
        The instance ID.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def platform(self) -> pulumi.Output[str]:
        """
        The distribution of the operating system for the system disk in the custom image. 
        If you specify a data disk snapshot to create the system disk of the custom image, you must use the Platform parameter
        to specify the distribution of the operating system for the system disk. Default value: Others Linux.
        More valid values refer to [CreateImage OpenAPI](https://www.alibabacloud.com/help/en/elastic-compute-service/latest/createimage)
        **NOTE**: It's default value is Ubuntu before version 1.197.0.
        """
        return pulumi.get(self, "platform")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the enterprise resource group to which a custom image belongs
        """
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter(name="snapshotId")
    def snapshot_id(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies a snapshot that is used to create a combined custom image.
        """
        return pulumi.get(self, "snapshot_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        The tag value of an image. The value of N ranges from 1 to 20.
        """
        return pulumi.get(self, "tags")

