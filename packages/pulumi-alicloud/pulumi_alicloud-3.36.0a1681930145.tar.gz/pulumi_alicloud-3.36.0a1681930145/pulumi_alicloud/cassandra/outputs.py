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
    'GetBackupPlansPlanResult',
    'GetClustersClusterResult',
    'GetDataCentersCenterResult',
    'GetZonesZoneResult',
]

@pulumi.output_type
class GetBackupPlansPlanResult(dict):
    def __init__(__self__, *,
                 active: bool,
                 backup_period: str,
                 backup_time: str,
                 cluster_id: str,
                 create_time: str,
                 data_center_id: str,
                 id: str,
                 retention_period: int):
        """
        :param bool active: Specifies whether to activate the backup plan.
        :param str backup_period: The backup cycle. Valid values: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, and Sunday.
        :param str backup_time: The start time of the backup task each day. The time is displayed in UTC and denoted by Z.
        :param str cluster_id: The ID of the cluster for the backup.
        :param str create_time: The time when the backup plan was created.
        :param str data_center_id: The ID of the data center for the backup in the cluster.
        :param str id: The ID of the Backup Plan.
        :param int retention_period: The duration for which you want to retain the backup. Valid values: 1 to 30. Unit: days.
        """
        pulumi.set(__self__, "active", active)
        pulumi.set(__self__, "backup_period", backup_period)
        pulumi.set(__self__, "backup_time", backup_time)
        pulumi.set(__self__, "cluster_id", cluster_id)
        pulumi.set(__self__, "create_time", create_time)
        pulumi.set(__self__, "data_center_id", data_center_id)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "retention_period", retention_period)

    @property
    @pulumi.getter
    def active(self) -> bool:
        """
        Specifies whether to activate the backup plan.
        """
        return pulumi.get(self, "active")

    @property
    @pulumi.getter(name="backupPeriod")
    def backup_period(self) -> str:
        """
        The backup cycle. Valid values: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, and Sunday.
        """
        return pulumi.get(self, "backup_period")

    @property
    @pulumi.getter(name="backupTime")
    def backup_time(self) -> str:
        """
        The start time of the backup task each day. The time is displayed in UTC and denoted by Z.
        """
        return pulumi.get(self, "backup_time")

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> str:
        """
        The ID of the cluster for the backup.
        """
        return pulumi.get(self, "cluster_id")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        The time when the backup plan was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="dataCenterId")
    def data_center_id(self) -> str:
        """
        The ID of the data center for the backup in the cluster.
        """
        return pulumi.get(self, "data_center_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the Backup Plan.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="retentionPeriod")
    def retention_period(self) -> int:
        """
        The duration for which you want to retain the backup. Valid values: 1 to 30. Unit: days.
        """
        return pulumi.get(self, "retention_period")


@pulumi.output_type
class GetClustersClusterResult(dict):
    def __init__(__self__, *,
                 cluster_id: str,
                 cluster_name: str,
                 created_time: str,
                 data_center_count: int,
                 expire_time: str,
                 id: str,
                 lock_mode: str,
                 major_version: str,
                 minor_version: str,
                 pay_type: str,
                 status: str,
                 tags: Optional[Mapping[str, Any]] = None):
        """
        :param str cluster_id: The ID of the Cassandra cluster.
        :param str cluster_name: The name of the Cassandra cluster.
        :param int data_center_count: The count of data centers
        :param str expire_time: The expire time of the cluster.
        :param str id: The ID of the Cassandra cluster.
        :param str lock_mode: The lock mode of the cluster.
        :param str major_version: The major version of the cluster.
        :param str minor_version: The minor version of the cluster.
        :param str pay_type: Billing method. Value options are `Subscription` for Pay-As-You-Go and `PayAsYouGo` for yearly or monthly subscription.
        :param str status: Status of the cluster.
        :param Mapping[str, Any] tags: A mapping of tags to assign to the resource.
        """
        pulumi.set(__self__, "cluster_id", cluster_id)
        pulumi.set(__self__, "cluster_name", cluster_name)
        pulumi.set(__self__, "created_time", created_time)
        pulumi.set(__self__, "data_center_count", data_center_count)
        pulumi.set(__self__, "expire_time", expire_time)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "lock_mode", lock_mode)
        pulumi.set(__self__, "major_version", major_version)
        pulumi.set(__self__, "minor_version", minor_version)
        pulumi.set(__self__, "pay_type", pay_type)
        pulumi.set(__self__, "status", status)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> str:
        """
        The ID of the Cassandra cluster.
        """
        return pulumi.get(self, "cluster_id")

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> str:
        """
        The name of the Cassandra cluster.
        """
        return pulumi.get(self, "cluster_name")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> str:
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter(name="dataCenterCount")
    def data_center_count(self) -> int:
        """
        The count of data centers
        """
        return pulumi.get(self, "data_center_count")

    @property
    @pulumi.getter(name="expireTime")
    def expire_time(self) -> str:
        """
        The expire time of the cluster.
        """
        return pulumi.get(self, "expire_time")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the Cassandra cluster.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lockMode")
    def lock_mode(self) -> str:
        """
        The lock mode of the cluster.
        """
        return pulumi.get(self, "lock_mode")

    @property
    @pulumi.getter(name="majorVersion")
    def major_version(self) -> str:
        """
        The major version of the cluster.
        """
        return pulumi.get(self, "major_version")

    @property
    @pulumi.getter(name="minorVersion")
    def minor_version(self) -> str:
        """
        The minor version of the cluster.
        """
        return pulumi.get(self, "minor_version")

    @property
    @pulumi.getter(name="payType")
    def pay_type(self) -> str:
        """
        Billing method. Value options are `Subscription` for Pay-As-You-Go and `PayAsYouGo` for yearly or monthly subscription.
        """
        return pulumi.get(self, "pay_type")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the cluster.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, Any]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")


@pulumi.output_type
class GetDataCentersCenterResult(dict):
    def __init__(__self__, *,
                 cluster_id: str,
                 commodity_instance: str,
                 created_time: str,
                 data_center_id: str,
                 data_center_name: str,
                 disk_size: int,
                 disk_type: str,
                 expire_time: str,
                 instance_type: str,
                 lock_mode: str,
                 node_count: int,
                 pay_type: str,
                 status: str,
                 vpc_id: str,
                 vswitch_id: str,
                 zone_id: str):
        """
        :param str cluster_id: The cluster id of dataCenters belongs to.
        :param str commodity_instance: The commodity ID of the Cassandra dataCenter.
        :param str data_center_id: The id of the Cassandra dataCenter.
        :param str data_center_name: The name of the Cassandra dataCenter.
        :param int disk_size: One node disk size, unit:GB.
        :param str disk_type: Cloud_ssd or cloud_efficiency.
        :param str expire_time: The expire time of the dataCenter.
        :param str instance_type: The instance type of the Cassandra dataCenter, eg: cassandra.c.large.
        :param str lock_mode: The lock mode of the dataCenter.
        :param int node_count: The node count of dataCenter.
        :param str pay_type: Billing method. Value options are `Subscription` for Pay-As-You-Go and `PayAsYouGo` for yearly or monthly subscription.
        :param str status: Status of the dataCenter.
        :param str vpc_id: VPC ID the dataCenter belongs to.
        :param str vswitch_id: VSwitch ID the dataCenter belongs to.
        :param str zone_id: Zone ID the dataCenter belongs to.
        """
        pulumi.set(__self__, "cluster_id", cluster_id)
        pulumi.set(__self__, "commodity_instance", commodity_instance)
        pulumi.set(__self__, "created_time", created_time)
        pulumi.set(__self__, "data_center_id", data_center_id)
        pulumi.set(__self__, "data_center_name", data_center_name)
        pulumi.set(__self__, "disk_size", disk_size)
        pulumi.set(__self__, "disk_type", disk_type)
        pulumi.set(__self__, "expire_time", expire_time)
        pulumi.set(__self__, "instance_type", instance_type)
        pulumi.set(__self__, "lock_mode", lock_mode)
        pulumi.set(__self__, "node_count", node_count)
        pulumi.set(__self__, "pay_type", pay_type)
        pulumi.set(__self__, "status", status)
        pulumi.set(__self__, "vpc_id", vpc_id)
        pulumi.set(__self__, "vswitch_id", vswitch_id)
        pulumi.set(__self__, "zone_id", zone_id)

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> str:
        """
        The cluster id of dataCenters belongs to.
        """
        return pulumi.get(self, "cluster_id")

    @property
    @pulumi.getter(name="commodityInstance")
    def commodity_instance(self) -> str:
        """
        The commodity ID of the Cassandra dataCenter.
        """
        return pulumi.get(self, "commodity_instance")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> str:
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter(name="dataCenterId")
    def data_center_id(self) -> str:
        """
        The id of the Cassandra dataCenter.
        """
        return pulumi.get(self, "data_center_id")

    @property
    @pulumi.getter(name="dataCenterName")
    def data_center_name(self) -> str:
        """
        The name of the Cassandra dataCenter.
        """
        return pulumi.get(self, "data_center_name")

    @property
    @pulumi.getter(name="diskSize")
    def disk_size(self) -> int:
        """
        One node disk size, unit:GB.
        """
        return pulumi.get(self, "disk_size")

    @property
    @pulumi.getter(name="diskType")
    def disk_type(self) -> str:
        """
        Cloud_ssd or cloud_efficiency.
        """
        return pulumi.get(self, "disk_type")

    @property
    @pulumi.getter(name="expireTime")
    def expire_time(self) -> str:
        """
        The expire time of the dataCenter.
        """
        return pulumi.get(self, "expire_time")

    @property
    @pulumi.getter(name="instanceType")
    def instance_type(self) -> str:
        """
        The instance type of the Cassandra dataCenter, eg: cassandra.c.large.
        """
        return pulumi.get(self, "instance_type")

    @property
    @pulumi.getter(name="lockMode")
    def lock_mode(self) -> str:
        """
        The lock mode of the dataCenter.
        """
        return pulumi.get(self, "lock_mode")

    @property
    @pulumi.getter(name="nodeCount")
    def node_count(self) -> int:
        """
        The node count of dataCenter.
        """
        return pulumi.get(self, "node_count")

    @property
    @pulumi.getter(name="payType")
    def pay_type(self) -> str:
        """
        Billing method. Value options are `Subscription` for Pay-As-You-Go and `PayAsYouGo` for yearly or monthly subscription.
        """
        return pulumi.get(self, "pay_type")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the dataCenter.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        """
        VPC ID the dataCenter belongs to.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="vswitchId")
    def vswitch_id(self) -> str:
        """
        VSwitch ID the dataCenter belongs to.
        """
        return pulumi.get(self, "vswitch_id")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> str:
        """
        Zone ID the dataCenter belongs to.
        """
        return pulumi.get(self, "zone_id")


@pulumi.output_type
class GetZonesZoneResult(dict):
    def __init__(__self__, *,
                 id: str,
                 multi_zone_ids: Sequence[str]):
        """
        :param str id: ID of the zone.
        :param Sequence[str] multi_zone_ids: A list of zone ids in which the multi zone.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "multi_zone_ids", multi_zone_ids)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        ID of the zone.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="multiZoneIds")
    def multi_zone_ids(self) -> Sequence[str]:
        """
        A list of zone ids in which the multi zone.
        """
        return pulumi.get(self, "multi_zone_ids")


