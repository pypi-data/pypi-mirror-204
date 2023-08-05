# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'ClusterBootstrapActionArgs',
    'ClusterConfigArgs',
    'ClusterHostGroupArgs',
    'ClusterMetaStoreConfArgs',
    'ClusterModifyClusterServiceConfigArgs',
]

@pulumi.input_type
class ClusterBootstrapActionArgs:
    def __init__(__self__, *,
                 arg: Optional[pulumi.Input[str]] = None,
                 execution_fail_strategy: Optional[pulumi.Input[str]] = None,
                 execution_moment: Optional[pulumi.Input[str]] = None,
                 execution_target: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 path: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] arg: bootstrap action args, e.g. "--a=b".
        :param pulumi.Input[str] execution_fail_strategy: bootstrap action execution fail strategy, ’FAILED_BLOCKED’ or ‘FAILED_CONTINUE’ . Default value: "FAILED_BLOCKED
        :param pulumi.Input[str] execution_moment: bootstrap action execution moment, ’BEFORE_INSTALL’ or ‘AFTER_STARTED’ . Default value: "BEFORE_INSTALL".
        :param pulumi.Input[str] execution_target: bootstrap action execution target, you can specify the host group name, e.g. "core_group". If this is not specified, the bootstrap action execution target is whole cluster.
        :param pulumi.Input[str] name: The name of emr cluster. The name length must be less than 64. Supported characters: chinese character, english character, number, "-", "_".
        :param pulumi.Input[str] path: bootstrap action path, e.g. "oss://bucket/path".
        """
        if arg is not None:
            pulumi.set(__self__, "arg", arg)
        if execution_fail_strategy is not None:
            pulumi.set(__self__, "execution_fail_strategy", execution_fail_strategy)
        if execution_moment is not None:
            pulumi.set(__self__, "execution_moment", execution_moment)
        if execution_target is not None:
            pulumi.set(__self__, "execution_target", execution_target)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if path is not None:
            pulumi.set(__self__, "path", path)

    @property
    @pulumi.getter
    def arg(self) -> Optional[pulumi.Input[str]]:
        """
        bootstrap action args, e.g. "--a=b".
        """
        return pulumi.get(self, "arg")

    @arg.setter
    def arg(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arg", value)

    @property
    @pulumi.getter(name="executionFailStrategy")
    def execution_fail_strategy(self) -> Optional[pulumi.Input[str]]:
        """
        bootstrap action execution fail strategy, ’FAILED_BLOCKED’ or ‘FAILED_CONTINUE’ . Default value: "FAILED_BLOCKED
        """
        return pulumi.get(self, "execution_fail_strategy")

    @execution_fail_strategy.setter
    def execution_fail_strategy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "execution_fail_strategy", value)

    @property
    @pulumi.getter(name="executionMoment")
    def execution_moment(self) -> Optional[pulumi.Input[str]]:
        """
        bootstrap action execution moment, ’BEFORE_INSTALL’ or ‘AFTER_STARTED’ . Default value: "BEFORE_INSTALL".
        """
        return pulumi.get(self, "execution_moment")

    @execution_moment.setter
    def execution_moment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "execution_moment", value)

    @property
    @pulumi.getter(name="executionTarget")
    def execution_target(self) -> Optional[pulumi.Input[str]]:
        """
        bootstrap action execution target, you can specify the host group name, e.g. "core_group". If this is not specified, the bootstrap action execution target is whole cluster.
        """
        return pulumi.get(self, "execution_target")

    @execution_target.setter
    def execution_target(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "execution_target", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of emr cluster. The name length must be less than 64. Supported characters: chinese character, english character, number, "-", "_".
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def path(self) -> Optional[pulumi.Input[str]]:
        """
        bootstrap action path, e.g. "oss://bucket/path".
        """
        return pulumi.get(self, "path")

    @path.setter
    def path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "path", value)


@pulumi.input_type
class ClusterConfigArgs:
    def __init__(__self__, *,
                 config_key: pulumi.Input[str],
                 config_value: pulumi.Input[str],
                 file_name: pulumi.Input[str],
                 service_name: pulumi.Input[str]):
        """
        :param pulumi.Input[str] config_key: Custom configuration service config key, e.g. ’dfs.replication’.
        :param pulumi.Input[str] config_value: Custom configuration service config value, e.g. ’3’.
        :param pulumi.Input[str] file_name: Custom configuration service file name, e.g. ’hdfs-site’.
        :param pulumi.Input[str] service_name: Custom configuration service name, e.g. ’HDFS’.
        """
        pulumi.set(__self__, "config_key", config_key)
        pulumi.set(__self__, "config_value", config_value)
        pulumi.set(__self__, "file_name", file_name)
        pulumi.set(__self__, "service_name", service_name)

    @property
    @pulumi.getter(name="configKey")
    def config_key(self) -> pulumi.Input[str]:
        """
        Custom configuration service config key, e.g. ’dfs.replication’.
        """
        return pulumi.get(self, "config_key")

    @config_key.setter
    def config_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "config_key", value)

    @property
    @pulumi.getter(name="configValue")
    def config_value(self) -> pulumi.Input[str]:
        """
        Custom configuration service config value, e.g. ’3’.
        """
        return pulumi.get(self, "config_value")

    @config_value.setter
    def config_value(self, value: pulumi.Input[str]):
        pulumi.set(self, "config_value", value)

    @property
    @pulumi.getter(name="fileName")
    def file_name(self) -> pulumi.Input[str]:
        """
        Custom configuration service file name, e.g. ’hdfs-site’.
        """
        return pulumi.get(self, "file_name")

    @file_name.setter
    def file_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "file_name", value)

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Input[str]:
        """
        Custom configuration service name, e.g. ’HDFS’.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_name", value)


@pulumi.input_type
class ClusterHostGroupArgs:
    def __init__(__self__, *,
                 auto_renew: Optional[pulumi.Input[bool]] = None,
                 charge_type: Optional[pulumi.Input[str]] = None,
                 decommission_timeout: Optional[pulumi.Input[int]] = None,
                 disk_capacity: Optional[pulumi.Input[str]] = None,
                 disk_count: Optional[pulumi.Input[str]] = None,
                 disk_type: Optional[pulumi.Input[str]] = None,
                 enable_graceful_decommission: Optional[pulumi.Input[bool]] = None,
                 gpu_driver: Optional[pulumi.Input[str]] = None,
                 host_group_name: Optional[pulumi.Input[str]] = None,
                 host_group_type: Optional[pulumi.Input[str]] = None,
                 instance_list: Optional[pulumi.Input[str]] = None,
                 instance_type: Optional[pulumi.Input[str]] = None,
                 node_count: Optional[pulumi.Input[str]] = None,
                 period: Optional[pulumi.Input[int]] = None,
                 sys_disk_capacity: Optional[pulumi.Input[str]] = None,
                 sys_disk_type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[bool] auto_renew: Auto renew for prepaid, ’true’ or ‘false’ . Default value: false.
        :param pulumi.Input[str] charge_type: Charge Type for this cluster. Supported value: PostPaid or PrePaid. Default value: PostPaid.
        :param pulumi.Input[int] decommission_timeout: Graceful decommission timeout, unit: seconds.
        :param pulumi.Input[str] disk_capacity: Data disk capacity.
        :param pulumi.Input[str] disk_count: Data disk count.
        :param pulumi.Input[str] disk_type: Data disk type. Supported value: cloud,cloud_efficiency,cloud_ssd,local_disk,cloud_essd.
        :param pulumi.Input[bool] enable_graceful_decommission: Enable hadoop cluster of task node graceful decommission, ’true’ or ‘false’ . Default value: false.
        :param pulumi.Input[str] host_group_name: host group name.
        :param pulumi.Input[str] host_group_type: host group type, supported value: MASTER, CORE or TASK, supported 'GATEWAY' available in 1.61.0+.
        :param pulumi.Input[str] instance_list: Instance list for cluster scale down. This value follows the json format, e.g. ["instance_id1","instance_id2"]. escape character for " is \\".
        :param pulumi.Input[str] instance_type: Host Ecs instance type.
        :param pulumi.Input[str] node_count: Host number in this group.
        :param pulumi.Input[int] period: If charge type is PrePaid, this should be specified, unit is month. Supported value: 1、2、3、4、5、6、7、8、9、12、24、36.
        :param pulumi.Input[str] sys_disk_capacity: System disk capacity.
        :param pulumi.Input[str] sys_disk_type: System disk type. Supported value: cloud,cloud_efficiency,cloud_ssd,cloud_essd.
        """
        if auto_renew is not None:
            pulumi.set(__self__, "auto_renew", auto_renew)
        if charge_type is not None:
            pulumi.set(__self__, "charge_type", charge_type)
        if decommission_timeout is not None:
            pulumi.set(__self__, "decommission_timeout", decommission_timeout)
        if disk_capacity is not None:
            pulumi.set(__self__, "disk_capacity", disk_capacity)
        if disk_count is not None:
            pulumi.set(__self__, "disk_count", disk_count)
        if disk_type is not None:
            pulumi.set(__self__, "disk_type", disk_type)
        if enable_graceful_decommission is not None:
            pulumi.set(__self__, "enable_graceful_decommission", enable_graceful_decommission)
        if gpu_driver is not None:
            pulumi.set(__self__, "gpu_driver", gpu_driver)
        if host_group_name is not None:
            pulumi.set(__self__, "host_group_name", host_group_name)
        if host_group_type is not None:
            pulumi.set(__self__, "host_group_type", host_group_type)
        if instance_list is not None:
            pulumi.set(__self__, "instance_list", instance_list)
        if instance_type is not None:
            pulumi.set(__self__, "instance_type", instance_type)
        if node_count is not None:
            pulumi.set(__self__, "node_count", node_count)
        if period is not None:
            pulumi.set(__self__, "period", period)
        if sys_disk_capacity is not None:
            pulumi.set(__self__, "sys_disk_capacity", sys_disk_capacity)
        if sys_disk_type is not None:
            pulumi.set(__self__, "sys_disk_type", sys_disk_type)

    @property
    @pulumi.getter(name="autoRenew")
    def auto_renew(self) -> Optional[pulumi.Input[bool]]:
        """
        Auto renew for prepaid, ’true’ or ‘false’ . Default value: false.
        """
        return pulumi.get(self, "auto_renew")

    @auto_renew.setter
    def auto_renew(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_renew", value)

    @property
    @pulumi.getter(name="chargeType")
    def charge_type(self) -> Optional[pulumi.Input[str]]:
        """
        Charge Type for this cluster. Supported value: PostPaid or PrePaid. Default value: PostPaid.
        """
        return pulumi.get(self, "charge_type")

    @charge_type.setter
    def charge_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "charge_type", value)

    @property
    @pulumi.getter(name="decommissionTimeout")
    def decommission_timeout(self) -> Optional[pulumi.Input[int]]:
        """
        Graceful decommission timeout, unit: seconds.
        """
        return pulumi.get(self, "decommission_timeout")

    @decommission_timeout.setter
    def decommission_timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "decommission_timeout", value)

    @property
    @pulumi.getter(name="diskCapacity")
    def disk_capacity(self) -> Optional[pulumi.Input[str]]:
        """
        Data disk capacity.
        """
        return pulumi.get(self, "disk_capacity")

    @disk_capacity.setter
    def disk_capacity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "disk_capacity", value)

    @property
    @pulumi.getter(name="diskCount")
    def disk_count(self) -> Optional[pulumi.Input[str]]:
        """
        Data disk count.
        """
        return pulumi.get(self, "disk_count")

    @disk_count.setter
    def disk_count(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "disk_count", value)

    @property
    @pulumi.getter(name="diskType")
    def disk_type(self) -> Optional[pulumi.Input[str]]:
        """
        Data disk type. Supported value: cloud,cloud_efficiency,cloud_ssd,local_disk,cloud_essd.
        """
        return pulumi.get(self, "disk_type")

    @disk_type.setter
    def disk_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "disk_type", value)

    @property
    @pulumi.getter(name="enableGracefulDecommission")
    def enable_graceful_decommission(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable hadoop cluster of task node graceful decommission, ’true’ or ‘false’ . Default value: false.
        """
        return pulumi.get(self, "enable_graceful_decommission")

    @enable_graceful_decommission.setter
    def enable_graceful_decommission(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_graceful_decommission", value)

    @property
    @pulumi.getter(name="gpuDriver")
    def gpu_driver(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "gpu_driver")

    @gpu_driver.setter
    def gpu_driver(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "gpu_driver", value)

    @property
    @pulumi.getter(name="hostGroupName")
    def host_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        host group name.
        """
        return pulumi.get(self, "host_group_name")

    @host_group_name.setter
    def host_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host_group_name", value)

    @property
    @pulumi.getter(name="hostGroupType")
    def host_group_type(self) -> Optional[pulumi.Input[str]]:
        """
        host group type, supported value: MASTER, CORE or TASK, supported 'GATEWAY' available in 1.61.0+.
        """
        return pulumi.get(self, "host_group_type")

    @host_group_type.setter
    def host_group_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host_group_type", value)

    @property
    @pulumi.getter(name="instanceList")
    def instance_list(self) -> Optional[pulumi.Input[str]]:
        """
        Instance list for cluster scale down. This value follows the json format, e.g. ["instance_id1","instance_id2"]. escape character for " is \\".
        """
        return pulumi.get(self, "instance_list")

    @instance_list.setter
    def instance_list(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_list", value)

    @property
    @pulumi.getter(name="instanceType")
    def instance_type(self) -> Optional[pulumi.Input[str]]:
        """
        Host Ecs instance type.
        """
        return pulumi.get(self, "instance_type")

    @instance_type.setter
    def instance_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_type", value)

    @property
    @pulumi.getter(name="nodeCount")
    def node_count(self) -> Optional[pulumi.Input[str]]:
        """
        Host number in this group.
        """
        return pulumi.get(self, "node_count")

    @node_count.setter
    def node_count(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "node_count", value)

    @property
    @pulumi.getter
    def period(self) -> Optional[pulumi.Input[int]]:
        """
        If charge type is PrePaid, this should be specified, unit is month. Supported value: 1、2、3、4、5、6、7、8、9、12、24、36.
        """
        return pulumi.get(self, "period")

    @period.setter
    def period(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "period", value)

    @property
    @pulumi.getter(name="sysDiskCapacity")
    def sys_disk_capacity(self) -> Optional[pulumi.Input[str]]:
        """
        System disk capacity.
        """
        return pulumi.get(self, "sys_disk_capacity")

    @sys_disk_capacity.setter
    def sys_disk_capacity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sys_disk_capacity", value)

    @property
    @pulumi.getter(name="sysDiskType")
    def sys_disk_type(self) -> Optional[pulumi.Input[str]]:
        """
        System disk type. Supported value: cloud,cloud_efficiency,cloud_ssd,cloud_essd.
        """
        return pulumi.get(self, "sys_disk_type")

    @sys_disk_type.setter
    def sys_disk_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sys_disk_type", value)


@pulumi.input_type
class ClusterMetaStoreConfArgs:
    def __init__(__self__, *,
                 db_password: pulumi.Input[str],
                 db_url: pulumi.Input[str],
                 db_user_name: pulumi.Input[str]):
        """
        :param pulumi.Input[str] db_password: Custom rds database password.
        :param pulumi.Input[str] db_url: Custom rds database connection url.
        :param pulumi.Input[str] db_user_name: Custom rds database user name.
        """
        pulumi.set(__self__, "db_password", db_password)
        pulumi.set(__self__, "db_url", db_url)
        pulumi.set(__self__, "db_user_name", db_user_name)

    @property
    @pulumi.getter(name="dbPassword")
    def db_password(self) -> pulumi.Input[str]:
        """
        Custom rds database password.
        """
        return pulumi.get(self, "db_password")

    @db_password.setter
    def db_password(self, value: pulumi.Input[str]):
        pulumi.set(self, "db_password", value)

    @property
    @pulumi.getter(name="dbUrl")
    def db_url(self) -> pulumi.Input[str]:
        """
        Custom rds database connection url.
        """
        return pulumi.get(self, "db_url")

    @db_url.setter
    def db_url(self, value: pulumi.Input[str]):
        pulumi.set(self, "db_url", value)

    @property
    @pulumi.getter(name="dbUserName")
    def db_user_name(self) -> pulumi.Input[str]:
        """
        Custom rds database user name.
        """
        return pulumi.get(self, "db_user_name")

    @db_user_name.setter
    def db_user_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "db_user_name", value)


@pulumi.input_type
class ClusterModifyClusterServiceConfigArgs:
    def __init__(__self__, *,
                 config_params: pulumi.Input[str],
                 service_name: pulumi.Input[str],
                 comment: Optional[pulumi.Input[str]] = None,
                 config_type: Optional[pulumi.Input[str]] = None,
                 custom_config_params: Optional[pulumi.Input[str]] = None,
                 gateway_cluster_id_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 host_instance_id: Optional[pulumi.Input[str]] = None,
                 refresh_host_config: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[str] config_params: Cluster service configuration modification params, e.g. ’{"hdfs-site":{"dfs.replication":"3"}}’.
        :param pulumi.Input[str] service_name: Custom configuration service name, e.g. ’HDFS’.
        :param pulumi.Input[str] comment: Cluster service configuration modification comment, e.g. "Modify tez configuration".
        :param pulumi.Input[str] config_type: Cluster service configuration modification type.
        :param pulumi.Input[str] custom_config_params: Cluster service configuration modification custom params, e.g. ’{"tez-site":{"key":{"Value":"value"}}}’.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] gateway_cluster_id_lists: Cluster service configuration modification related gateway cluster id list.
        :param pulumi.Input[str] group_id: Cluster service configuration modification node group id, e.g. ’G-XXX’.
        :param pulumi.Input[str] host_instance_id: Cluster service configuration modification host instance id, e.g. ’i-bp146tnrkq4tcxxxxx’.
        :param pulumi.Input[bool] refresh_host_config: Cluster service configuration modification refresh host config, ’true’ or ’false’.
        """
        pulumi.set(__self__, "config_params", config_params)
        pulumi.set(__self__, "service_name", service_name)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if config_type is not None:
            pulumi.set(__self__, "config_type", config_type)
        if custom_config_params is not None:
            pulumi.set(__self__, "custom_config_params", custom_config_params)
        if gateway_cluster_id_lists is not None:
            pulumi.set(__self__, "gateway_cluster_id_lists", gateway_cluster_id_lists)
        if group_id is not None:
            pulumi.set(__self__, "group_id", group_id)
        if host_instance_id is not None:
            pulumi.set(__self__, "host_instance_id", host_instance_id)
        if refresh_host_config is not None:
            pulumi.set(__self__, "refresh_host_config", refresh_host_config)

    @property
    @pulumi.getter(name="configParams")
    def config_params(self) -> pulumi.Input[str]:
        """
        Cluster service configuration modification params, e.g. ’{"hdfs-site":{"dfs.replication":"3"}}’.
        """
        return pulumi.get(self, "config_params")

    @config_params.setter
    def config_params(self, value: pulumi.Input[str]):
        pulumi.set(self, "config_params", value)

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Input[str]:
        """
        Custom configuration service name, e.g. ’HDFS’.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_name", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        Cluster service configuration modification comment, e.g. "Modify tez configuration".
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="configType")
    def config_type(self) -> Optional[pulumi.Input[str]]:
        """
        Cluster service configuration modification type.
        """
        return pulumi.get(self, "config_type")

    @config_type.setter
    def config_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "config_type", value)

    @property
    @pulumi.getter(name="customConfigParams")
    def custom_config_params(self) -> Optional[pulumi.Input[str]]:
        """
        Cluster service configuration modification custom params, e.g. ’{"tez-site":{"key":{"Value":"value"}}}’.
        """
        return pulumi.get(self, "custom_config_params")

    @custom_config_params.setter
    def custom_config_params(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_config_params", value)

    @property
    @pulumi.getter(name="gatewayClusterIdLists")
    def gateway_cluster_id_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Cluster service configuration modification related gateway cluster id list.
        """
        return pulumi.get(self, "gateway_cluster_id_lists")

    @gateway_cluster_id_lists.setter
    def gateway_cluster_id_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "gateway_cluster_id_lists", value)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[pulumi.Input[str]]:
        """
        Cluster service configuration modification node group id, e.g. ’G-XXX’.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="hostInstanceId")
    def host_instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        Cluster service configuration modification host instance id, e.g. ’i-bp146tnrkq4tcxxxxx’.
        """
        return pulumi.get(self, "host_instance_id")

    @host_instance_id.setter
    def host_instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host_instance_id", value)

    @property
    @pulumi.getter(name="refreshHostConfig")
    def refresh_host_config(self) -> Optional[pulumi.Input[bool]]:
        """
        Cluster service configuration modification refresh host config, ’true’ or ’false’.
        """
        return pulumi.get(self, "refresh_host_config")

    @refresh_host_config.setter
    def refresh_host_config(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "refresh_host_config", value)


