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
    'GetExchangesResult',
    'AwaitableGetExchangesResult',
    'get_exchanges',
    'get_exchanges_output',
]

@pulumi.output_type
class GetExchangesResult:
    """
    A collection of values returned by getExchanges.
    """
    def __init__(__self__, exchanges=None, id=None, ids=None, instance_id=None, name_regex=None, names=None, output_file=None, virtual_host_name=None):
        if exchanges and not isinstance(exchanges, list):
            raise TypeError("Expected argument 'exchanges' to be a list")
        pulumi.set(__self__, "exchanges", exchanges)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if instance_id and not isinstance(instance_id, str):
            raise TypeError("Expected argument 'instance_id' to be a str")
        pulumi.set(__self__, "instance_id", instance_id)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if virtual_host_name and not isinstance(virtual_host_name, str):
            raise TypeError("Expected argument 'virtual_host_name' to be a str")
        pulumi.set(__self__, "virtual_host_name", virtual_host_name)

    @property
    @pulumi.getter
    def exchanges(self) -> Sequence['outputs.GetExchangesExchangeResult']:
        return pulumi.get(self, "exchanges")

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
        return pulumi.get(self, "instance_id")

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
    @pulumi.getter(name="virtualHostName")
    def virtual_host_name(self) -> str:
        return pulumi.get(self, "virtual_host_name")


class AwaitableGetExchangesResult(GetExchangesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetExchangesResult(
            exchanges=self.exchanges,
            id=self.id,
            ids=self.ids,
            instance_id=self.instance_id,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            virtual_host_name=self.virtual_host_name)


def get_exchanges(ids: Optional[Sequence[str]] = None,
                  instance_id: Optional[str] = None,
                  name_regex: Optional[str] = None,
                  output_file: Optional[str] = None,
                  virtual_host_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetExchangesResult:
    """
    This data source provides the Amqp Exchanges of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.128.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.amqp.get_exchanges(instance_id="amqp-abc12345",
        virtual_host_name="my-VirtualHost",
        ids=[
            "my-Exchange-1",
            "my-Exchange-2",
        ])
    pulumi.export("amqpExchangeId1", ids.exchanges[0].id)
    name_regex = alicloud.amqp.get_exchanges(instance_id="amqp-abc12345",
        virtual_host_name="my-VirtualHost",
        name_regex="^my-Exchange")
    pulumi.export("amqpExchangeId2", name_regex.exchanges[0].id)
    ```


    :param Sequence[str] ids: A list of Exchange IDs. Its element value is same as Exchange Name.
    :param str instance_id: The ID of the instance.
    :param str name_regex: A regex string to filter results by Exchange name.
    :param str virtual_host_name: The name of virtual host where an exchange resides.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['instanceId'] = instance_id
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['virtualHostName'] = virtual_host_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:amqp/getExchanges:getExchanges', __args__, opts=opts, typ=GetExchangesResult).value

    return AwaitableGetExchangesResult(
        exchanges=__ret__.exchanges,
        id=__ret__.id,
        ids=__ret__.ids,
        instance_id=__ret__.instance_id,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file,
        virtual_host_name=__ret__.virtual_host_name)


@_utilities.lift_output_func(get_exchanges)
def get_exchanges_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                         instance_id: Optional[pulumi.Input[str]] = None,
                         name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                         output_file: Optional[pulumi.Input[Optional[str]]] = None,
                         virtual_host_name: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetExchangesResult]:
    """
    This data source provides the Amqp Exchanges of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.128.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.amqp.get_exchanges(instance_id="amqp-abc12345",
        virtual_host_name="my-VirtualHost",
        ids=[
            "my-Exchange-1",
            "my-Exchange-2",
        ])
    pulumi.export("amqpExchangeId1", ids.exchanges[0].id)
    name_regex = alicloud.amqp.get_exchanges(instance_id="amqp-abc12345",
        virtual_host_name="my-VirtualHost",
        name_regex="^my-Exchange")
    pulumi.export("amqpExchangeId2", name_regex.exchanges[0].id)
    ```


    :param Sequence[str] ids: A list of Exchange IDs. Its element value is same as Exchange Name.
    :param str instance_id: The ID of the instance.
    :param str name_regex: A regex string to filter results by Exchange name.
    :param str virtual_host_name: The name of virtual host where an exchange resides.
    """
    ...
