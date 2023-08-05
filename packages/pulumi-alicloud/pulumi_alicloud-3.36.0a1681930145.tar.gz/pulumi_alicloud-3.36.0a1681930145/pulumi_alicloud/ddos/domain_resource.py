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

__all__ = ['DomainResourceArgs', 'DomainResource']

@pulumi.input_type
class DomainResourceArgs:
    def __init__(__self__, *,
                 domain: pulumi.Input[str],
                 instance_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 proxy_types: pulumi.Input[Sequence[pulumi.Input['DomainResourceProxyTypeArgs']]],
                 real_servers: pulumi.Input[Sequence[pulumi.Input[str]]],
                 rs_type: pulumi.Input[int],
                 https_ext: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DomainResource resource.
        :param pulumi.Input[str] domain: The domain name of the website that you want to add to the instance.
        :param pulumi.Input[Sequence[pulumi.Input['DomainResourceProxyTypeArgs']]] proxy_types: Protocol type and port number information.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] real_servers: the IP address. This field is required and must be a string array.
        :param pulumi.Input[int] rs_type: The address type of the origin server. Valid values: `0`: IP address. `1`: domain name. Use the domain name of the origin server if you deploy proxies, such as Web Application Firewall (WAF), between the origin server and the Anti-DDoS Pro or Anti-DDoS Premium instance. If you use the domain name, you must enter the address of the proxy, such as the CNAME of WAF.
        :param pulumi.Input[str] https_ext: The advanced HTTPS settings. This parameter takes effect only when the value of ProxyType includes https. This parameter is a string that contains a JSON struct. The JSON struct includes the following fields:
        """
        pulumi.set(__self__, "domain", domain)
        pulumi.set(__self__, "instance_ids", instance_ids)
        pulumi.set(__self__, "proxy_types", proxy_types)
        pulumi.set(__self__, "real_servers", real_servers)
        pulumi.set(__self__, "rs_type", rs_type)
        if https_ext is not None:
            pulumi.set(__self__, "https_ext", https_ext)

    @property
    @pulumi.getter
    def domain(self) -> pulumi.Input[str]:
        """
        The domain name of the website that you want to add to the instance.
        """
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: pulumi.Input[str]):
        pulumi.set(self, "domain", value)

    @property
    @pulumi.getter(name="instanceIds")
    def instance_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        return pulumi.get(self, "instance_ids")

    @instance_ids.setter
    def instance_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "instance_ids", value)

    @property
    @pulumi.getter(name="proxyTypes")
    def proxy_types(self) -> pulumi.Input[Sequence[pulumi.Input['DomainResourceProxyTypeArgs']]]:
        """
        Protocol type and port number information.
        """
        return pulumi.get(self, "proxy_types")

    @proxy_types.setter
    def proxy_types(self, value: pulumi.Input[Sequence[pulumi.Input['DomainResourceProxyTypeArgs']]]):
        pulumi.set(self, "proxy_types", value)

    @property
    @pulumi.getter(name="realServers")
    def real_servers(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        the IP address. This field is required and must be a string array.
        """
        return pulumi.get(self, "real_servers")

    @real_servers.setter
    def real_servers(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "real_servers", value)

    @property
    @pulumi.getter(name="rsType")
    def rs_type(self) -> pulumi.Input[int]:
        """
        The address type of the origin server. Valid values: `0`: IP address. `1`: domain name. Use the domain name of the origin server if you deploy proxies, such as Web Application Firewall (WAF), between the origin server and the Anti-DDoS Pro or Anti-DDoS Premium instance. If you use the domain name, you must enter the address of the proxy, such as the CNAME of WAF.
        """
        return pulumi.get(self, "rs_type")

    @rs_type.setter
    def rs_type(self, value: pulumi.Input[int]):
        pulumi.set(self, "rs_type", value)

    @property
    @pulumi.getter(name="httpsExt")
    def https_ext(self) -> Optional[pulumi.Input[str]]:
        """
        The advanced HTTPS settings. This parameter takes effect only when the value of ProxyType includes https. This parameter is a string that contains a JSON struct. The JSON struct includes the following fields:
        """
        return pulumi.get(self, "https_ext")

    @https_ext.setter
    def https_ext(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "https_ext", value)


@pulumi.input_type
class _DomainResourceState:
    def __init__(__self__, *,
                 domain: Optional[pulumi.Input[str]] = None,
                 https_ext: Optional[pulumi.Input[str]] = None,
                 instance_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 proxy_types: Optional[pulumi.Input[Sequence[pulumi.Input['DomainResourceProxyTypeArgs']]]] = None,
                 real_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 rs_type: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering DomainResource resources.
        :param pulumi.Input[str] domain: The domain name of the website that you want to add to the instance.
        :param pulumi.Input[str] https_ext: The advanced HTTPS settings. This parameter takes effect only when the value of ProxyType includes https. This parameter is a string that contains a JSON struct. The JSON struct includes the following fields:
        :param pulumi.Input[Sequence[pulumi.Input['DomainResourceProxyTypeArgs']]] proxy_types: Protocol type and port number information.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] real_servers: the IP address. This field is required and must be a string array.
        :param pulumi.Input[int] rs_type: The address type of the origin server. Valid values: `0`: IP address. `1`: domain name. Use the domain name of the origin server if you deploy proxies, such as Web Application Firewall (WAF), between the origin server and the Anti-DDoS Pro or Anti-DDoS Premium instance. If you use the domain name, you must enter the address of the proxy, such as the CNAME of WAF.
        """
        if domain is not None:
            pulumi.set(__self__, "domain", domain)
        if https_ext is not None:
            pulumi.set(__self__, "https_ext", https_ext)
        if instance_ids is not None:
            pulumi.set(__self__, "instance_ids", instance_ids)
        if proxy_types is not None:
            pulumi.set(__self__, "proxy_types", proxy_types)
        if real_servers is not None:
            pulumi.set(__self__, "real_servers", real_servers)
        if rs_type is not None:
            pulumi.set(__self__, "rs_type", rs_type)

    @property
    @pulumi.getter
    def domain(self) -> Optional[pulumi.Input[str]]:
        """
        The domain name of the website that you want to add to the instance.
        """
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain", value)

    @property
    @pulumi.getter(name="httpsExt")
    def https_ext(self) -> Optional[pulumi.Input[str]]:
        """
        The advanced HTTPS settings. This parameter takes effect only when the value of ProxyType includes https. This parameter is a string that contains a JSON struct. The JSON struct includes the following fields:
        """
        return pulumi.get(self, "https_ext")

    @https_ext.setter
    def https_ext(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "https_ext", value)

    @property
    @pulumi.getter(name="instanceIds")
    def instance_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "instance_ids")

    @instance_ids.setter
    def instance_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "instance_ids", value)

    @property
    @pulumi.getter(name="proxyTypes")
    def proxy_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DomainResourceProxyTypeArgs']]]]:
        """
        Protocol type and port number information.
        """
        return pulumi.get(self, "proxy_types")

    @proxy_types.setter
    def proxy_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DomainResourceProxyTypeArgs']]]]):
        pulumi.set(self, "proxy_types", value)

    @property
    @pulumi.getter(name="realServers")
    def real_servers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        the IP address. This field is required and must be a string array.
        """
        return pulumi.get(self, "real_servers")

    @real_servers.setter
    def real_servers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "real_servers", value)

    @property
    @pulumi.getter(name="rsType")
    def rs_type(self) -> Optional[pulumi.Input[int]]:
        """
        The address type of the origin server. Valid values: `0`: IP address. `1`: domain name. Use the domain name of the origin server if you deploy proxies, such as Web Application Firewall (WAF), between the origin server and the Anti-DDoS Pro or Anti-DDoS Premium instance. If you use the domain name, you must enter the address of the proxy, such as the CNAME of WAF.
        """
        return pulumi.get(self, "rs_type")

    @rs_type.setter
    def rs_type(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "rs_type", value)


class DomainResource(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 https_ext: Optional[pulumi.Input[str]] = None,
                 instance_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 proxy_types: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DomainResourceProxyTypeArgs']]]]] = None,
                 real_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 rs_type: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Provides a Anti-DDoS Pro Domain Resource resource.

        For information about Anti-DDoS Pro Domain Resource and how to use it, see [What is Domain Resource](https://www.alibabacloud.com/help/en/doc-detail/157463.htm).

        > **NOTE:** Available in v1.123.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example = alicloud.ddos.DomainResource("example",
            domain="tftestacc1234.abc",
            https_ext="{\\"Http2\\":1,\\"Http2https\\":0，\\"Https2http\\":0}",
            instance_ids=["ddoscoo-cn-6ja1rl4j****"],
            proxy_types=[alicloud.ddos.DomainResourceProxyTypeArgs(
                proxy_ports=[443],
                proxy_type="https",
            )],
            real_servers=["177.167.32.11"],
            rs_type=0)
        ```

        ## Import

        Anti-DDoS Pro Domain Resource can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:ddos/domainResource:DomainResource example <domain>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] domain: The domain name of the website that you want to add to the instance.
        :param pulumi.Input[str] https_ext: The advanced HTTPS settings. This parameter takes effect only when the value of ProxyType includes https. This parameter is a string that contains a JSON struct. The JSON struct includes the following fields:
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DomainResourceProxyTypeArgs']]]] proxy_types: Protocol type and port number information.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] real_servers: the IP address. This field is required and must be a string array.
        :param pulumi.Input[int] rs_type: The address type of the origin server. Valid values: `0`: IP address. `1`: domain name. Use the domain name of the origin server if you deploy proxies, such as Web Application Firewall (WAF), between the origin server and the Anti-DDoS Pro or Anti-DDoS Premium instance. If you use the domain name, you must enter the address of the proxy, such as the CNAME of WAF.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DomainResourceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Anti-DDoS Pro Domain Resource resource.

        For information about Anti-DDoS Pro Domain Resource and how to use it, see [What is Domain Resource](https://www.alibabacloud.com/help/en/doc-detail/157463.htm).

        > **NOTE:** Available in v1.123.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example = alicloud.ddos.DomainResource("example",
            domain="tftestacc1234.abc",
            https_ext="{\\"Http2\\":1,\\"Http2https\\":0，\\"Https2http\\":0}",
            instance_ids=["ddoscoo-cn-6ja1rl4j****"],
            proxy_types=[alicloud.ddos.DomainResourceProxyTypeArgs(
                proxy_ports=[443],
                proxy_type="https",
            )],
            real_servers=["177.167.32.11"],
            rs_type=0)
        ```

        ## Import

        Anti-DDoS Pro Domain Resource can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:ddos/domainResource:DomainResource example <domain>
        ```

        :param str resource_name: The name of the resource.
        :param DomainResourceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DomainResourceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 https_ext: Optional[pulumi.Input[str]] = None,
                 instance_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 proxy_types: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DomainResourceProxyTypeArgs']]]]] = None,
                 real_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 rs_type: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DomainResourceArgs.__new__(DomainResourceArgs)

            if domain is None and not opts.urn:
                raise TypeError("Missing required property 'domain'")
            __props__.__dict__["domain"] = domain
            __props__.__dict__["https_ext"] = https_ext
            if instance_ids is None and not opts.urn:
                raise TypeError("Missing required property 'instance_ids'")
            __props__.__dict__["instance_ids"] = instance_ids
            if proxy_types is None and not opts.urn:
                raise TypeError("Missing required property 'proxy_types'")
            __props__.__dict__["proxy_types"] = proxy_types
            if real_servers is None and not opts.urn:
                raise TypeError("Missing required property 'real_servers'")
            __props__.__dict__["real_servers"] = real_servers
            if rs_type is None and not opts.urn:
                raise TypeError("Missing required property 'rs_type'")
            __props__.__dict__["rs_type"] = rs_type
        super(DomainResource, __self__).__init__(
            'alicloud:ddos/domainResource:DomainResource',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            domain: Optional[pulumi.Input[str]] = None,
            https_ext: Optional[pulumi.Input[str]] = None,
            instance_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            proxy_types: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DomainResourceProxyTypeArgs']]]]] = None,
            real_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            rs_type: Optional[pulumi.Input[int]] = None) -> 'DomainResource':
        """
        Get an existing DomainResource resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] domain: The domain name of the website that you want to add to the instance.
        :param pulumi.Input[str] https_ext: The advanced HTTPS settings. This parameter takes effect only when the value of ProxyType includes https. This parameter is a string that contains a JSON struct. The JSON struct includes the following fields:
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DomainResourceProxyTypeArgs']]]] proxy_types: Protocol type and port number information.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] real_servers: the IP address. This field is required and must be a string array.
        :param pulumi.Input[int] rs_type: The address type of the origin server. Valid values: `0`: IP address. `1`: domain name. Use the domain name of the origin server if you deploy proxies, such as Web Application Firewall (WAF), between the origin server and the Anti-DDoS Pro or Anti-DDoS Premium instance. If you use the domain name, you must enter the address of the proxy, such as the CNAME of WAF.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DomainResourceState.__new__(_DomainResourceState)

        __props__.__dict__["domain"] = domain
        __props__.__dict__["https_ext"] = https_ext
        __props__.__dict__["instance_ids"] = instance_ids
        __props__.__dict__["proxy_types"] = proxy_types
        __props__.__dict__["real_servers"] = real_servers
        __props__.__dict__["rs_type"] = rs_type
        return DomainResource(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def domain(self) -> pulumi.Output[str]:
        """
        The domain name of the website that you want to add to the instance.
        """
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter(name="httpsExt")
    def https_ext(self) -> pulumi.Output[str]:
        """
        The advanced HTTPS settings. This parameter takes effect only when the value of ProxyType includes https. This parameter is a string that contains a JSON struct. The JSON struct includes the following fields:
        """
        return pulumi.get(self, "https_ext")

    @property
    @pulumi.getter(name="instanceIds")
    def instance_ids(self) -> pulumi.Output[Sequence[str]]:
        return pulumi.get(self, "instance_ids")

    @property
    @pulumi.getter(name="proxyTypes")
    def proxy_types(self) -> pulumi.Output[Sequence['outputs.DomainResourceProxyType']]:
        """
        Protocol type and port number information.
        """
        return pulumi.get(self, "proxy_types")

    @property
    @pulumi.getter(name="realServers")
    def real_servers(self) -> pulumi.Output[Sequence[str]]:
        """
        the IP address. This field is required and must be a string array.
        """
        return pulumi.get(self, "real_servers")

    @property
    @pulumi.getter(name="rsType")
    def rs_type(self) -> pulumi.Output[int]:
        """
        The address type of the origin server. Valid values: `0`: IP address. `1`: domain name. Use the domain name of the origin server if you deploy proxies, such as Web Application Firewall (WAF), between the origin server and the Anti-DDoS Pro or Anti-DDoS Premium instance. If you use the domain name, you must enter the address of the proxy, such as the CNAME of WAF.
        """
        return pulumi.get(self, "rs_type")

