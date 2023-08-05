# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['OrderArgs', 'Order']

@pulumi.input_type
class OrderArgs:
    def __init__(__self__, *,
                 package_version: pulumi.Input[str],
                 pricing_cycle: pulumi.Input[str],
                 product_code: pulumi.Input[str],
                 components: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 coupon_id: Optional[pulumi.Input[str]] = None,
                 duration: Optional[pulumi.Input[int]] = None,
                 pay_type: Optional[pulumi.Input[str]] = None,
                 quantity: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a Order resource.
        :param pulumi.Input[str] package_version: The package version of the market product.
        :param pulumi.Input[str] pricing_cycle: The purchase cycle of the product, valid values are `Day`, `Month` and `Year`.
        :param pulumi.Input[str] product_code: The product_code of market place product.
        :param pulumi.Input[Mapping[str, Any]] components: Service providers customize additional components.
        :param pulumi.Input[str] coupon_id: The coupon id of the market product.
        :param pulumi.Input[int] duration: The number of purchase cycles.
        :param pulumi.Input[str] pay_type: Valid values are `PrePaid`, `PostPaid`,System default to `PostPaid`.
        :param pulumi.Input[int] quantity: The quantity of the market product will be purchased.
        """
        pulumi.set(__self__, "package_version", package_version)
        pulumi.set(__self__, "pricing_cycle", pricing_cycle)
        pulumi.set(__self__, "product_code", product_code)
        if components is not None:
            pulumi.set(__self__, "components", components)
        if coupon_id is not None:
            pulumi.set(__self__, "coupon_id", coupon_id)
        if duration is not None:
            pulumi.set(__self__, "duration", duration)
        if pay_type is not None:
            pulumi.set(__self__, "pay_type", pay_type)
        if quantity is not None:
            pulumi.set(__self__, "quantity", quantity)

    @property
    @pulumi.getter(name="packageVersion")
    def package_version(self) -> pulumi.Input[str]:
        """
        The package version of the market product.
        """
        return pulumi.get(self, "package_version")

    @package_version.setter
    def package_version(self, value: pulumi.Input[str]):
        pulumi.set(self, "package_version", value)

    @property
    @pulumi.getter(name="pricingCycle")
    def pricing_cycle(self) -> pulumi.Input[str]:
        """
        The purchase cycle of the product, valid values are `Day`, `Month` and `Year`.
        """
        return pulumi.get(self, "pricing_cycle")

    @pricing_cycle.setter
    def pricing_cycle(self, value: pulumi.Input[str]):
        pulumi.set(self, "pricing_cycle", value)

    @property
    @pulumi.getter(name="productCode")
    def product_code(self) -> pulumi.Input[str]:
        """
        The product_code of market place product.
        """
        return pulumi.get(self, "product_code")

    @product_code.setter
    def product_code(self, value: pulumi.Input[str]):
        pulumi.set(self, "product_code", value)

    @property
    @pulumi.getter
    def components(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        Service providers customize additional components.
        """
        return pulumi.get(self, "components")

    @components.setter
    def components(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "components", value)

    @property
    @pulumi.getter(name="couponId")
    def coupon_id(self) -> Optional[pulumi.Input[str]]:
        """
        The coupon id of the market product.
        """
        return pulumi.get(self, "coupon_id")

    @coupon_id.setter
    def coupon_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "coupon_id", value)

    @property
    @pulumi.getter
    def duration(self) -> Optional[pulumi.Input[int]]:
        """
        The number of purchase cycles.
        """
        return pulumi.get(self, "duration")

    @duration.setter
    def duration(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "duration", value)

    @property
    @pulumi.getter(name="payType")
    def pay_type(self) -> Optional[pulumi.Input[str]]:
        """
        Valid values are `PrePaid`, `PostPaid`,System default to `PostPaid`.
        """
        return pulumi.get(self, "pay_type")

    @pay_type.setter
    def pay_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pay_type", value)

    @property
    @pulumi.getter
    def quantity(self) -> Optional[pulumi.Input[int]]:
        """
        The quantity of the market product will be purchased.
        """
        return pulumi.get(self, "quantity")

    @quantity.setter
    def quantity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "quantity", value)


@pulumi.input_type
class _OrderState:
    def __init__(__self__, *,
                 components: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 coupon_id: Optional[pulumi.Input[str]] = None,
                 duration: Optional[pulumi.Input[int]] = None,
                 package_version: Optional[pulumi.Input[str]] = None,
                 pay_type: Optional[pulumi.Input[str]] = None,
                 pricing_cycle: Optional[pulumi.Input[str]] = None,
                 product_code: Optional[pulumi.Input[str]] = None,
                 quantity: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering Order resources.
        :param pulumi.Input[Mapping[str, Any]] components: Service providers customize additional components.
        :param pulumi.Input[str] coupon_id: The coupon id of the market product.
        :param pulumi.Input[int] duration: The number of purchase cycles.
        :param pulumi.Input[str] package_version: The package version of the market product.
        :param pulumi.Input[str] pay_type: Valid values are `PrePaid`, `PostPaid`,System default to `PostPaid`.
        :param pulumi.Input[str] pricing_cycle: The purchase cycle of the product, valid values are `Day`, `Month` and `Year`.
        :param pulumi.Input[str] product_code: The product_code of market place product.
        :param pulumi.Input[int] quantity: The quantity of the market product will be purchased.
        """
        if components is not None:
            pulumi.set(__self__, "components", components)
        if coupon_id is not None:
            pulumi.set(__self__, "coupon_id", coupon_id)
        if duration is not None:
            pulumi.set(__self__, "duration", duration)
        if package_version is not None:
            pulumi.set(__self__, "package_version", package_version)
        if pay_type is not None:
            pulumi.set(__self__, "pay_type", pay_type)
        if pricing_cycle is not None:
            pulumi.set(__self__, "pricing_cycle", pricing_cycle)
        if product_code is not None:
            pulumi.set(__self__, "product_code", product_code)
        if quantity is not None:
            pulumi.set(__self__, "quantity", quantity)

    @property
    @pulumi.getter
    def components(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        Service providers customize additional components.
        """
        return pulumi.get(self, "components")

    @components.setter
    def components(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "components", value)

    @property
    @pulumi.getter(name="couponId")
    def coupon_id(self) -> Optional[pulumi.Input[str]]:
        """
        The coupon id of the market product.
        """
        return pulumi.get(self, "coupon_id")

    @coupon_id.setter
    def coupon_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "coupon_id", value)

    @property
    @pulumi.getter
    def duration(self) -> Optional[pulumi.Input[int]]:
        """
        The number of purchase cycles.
        """
        return pulumi.get(self, "duration")

    @duration.setter
    def duration(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "duration", value)

    @property
    @pulumi.getter(name="packageVersion")
    def package_version(self) -> Optional[pulumi.Input[str]]:
        """
        The package version of the market product.
        """
        return pulumi.get(self, "package_version")

    @package_version.setter
    def package_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "package_version", value)

    @property
    @pulumi.getter(name="payType")
    def pay_type(self) -> Optional[pulumi.Input[str]]:
        """
        Valid values are `PrePaid`, `PostPaid`,System default to `PostPaid`.
        """
        return pulumi.get(self, "pay_type")

    @pay_type.setter
    def pay_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pay_type", value)

    @property
    @pulumi.getter(name="pricingCycle")
    def pricing_cycle(self) -> Optional[pulumi.Input[str]]:
        """
        The purchase cycle of the product, valid values are `Day`, `Month` and `Year`.
        """
        return pulumi.get(self, "pricing_cycle")

    @pricing_cycle.setter
    def pricing_cycle(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pricing_cycle", value)

    @property
    @pulumi.getter(name="productCode")
    def product_code(self) -> Optional[pulumi.Input[str]]:
        """
        The product_code of market place product.
        """
        return pulumi.get(self, "product_code")

    @product_code.setter
    def product_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "product_code", value)

    @property
    @pulumi.getter
    def quantity(self) -> Optional[pulumi.Input[int]]:
        """
        The quantity of the market product will be purchased.
        """
        return pulumi.get(self, "quantity")

    @quantity.setter
    def quantity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "quantity", value)


class Order(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 components: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 coupon_id: Optional[pulumi.Input[str]] = None,
                 duration: Optional[pulumi.Input[int]] = None,
                 package_version: Optional[pulumi.Input[str]] = None,
                 pay_type: Optional[pulumi.Input[str]] = None,
                 pricing_cycle: Optional[pulumi.Input[str]] = None,
                 product_code: Optional[pulumi.Input[str]] = None,
                 quantity: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        order = alicloud.marketplace.Order("order",
            coupon_id="",
            duration=1,
            package_version="yuncode2713600001",
            pay_type="prepay",
            pricing_cycle="Month",
            product_code="cmapi033136",
            quantity=1)
        ```

        ## Import

        Market order can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:marketplace/order:Order order your-order-id
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, Any]] components: Service providers customize additional components.
        :param pulumi.Input[str] coupon_id: The coupon id of the market product.
        :param pulumi.Input[int] duration: The number of purchase cycles.
        :param pulumi.Input[str] package_version: The package version of the market product.
        :param pulumi.Input[str] pay_type: Valid values are `PrePaid`, `PostPaid`,System default to `PostPaid`.
        :param pulumi.Input[str] pricing_cycle: The purchase cycle of the product, valid values are `Day`, `Month` and `Year`.
        :param pulumi.Input[str] product_code: The product_code of market place product.
        :param pulumi.Input[int] quantity: The quantity of the market product will be purchased.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OrderArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        order = alicloud.marketplace.Order("order",
            coupon_id="",
            duration=1,
            package_version="yuncode2713600001",
            pay_type="prepay",
            pricing_cycle="Month",
            product_code="cmapi033136",
            quantity=1)
        ```

        ## Import

        Market order can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:marketplace/order:Order order your-order-id
        ```

        :param str resource_name: The name of the resource.
        :param OrderArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OrderArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 components: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 coupon_id: Optional[pulumi.Input[str]] = None,
                 duration: Optional[pulumi.Input[int]] = None,
                 package_version: Optional[pulumi.Input[str]] = None,
                 pay_type: Optional[pulumi.Input[str]] = None,
                 pricing_cycle: Optional[pulumi.Input[str]] = None,
                 product_code: Optional[pulumi.Input[str]] = None,
                 quantity: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OrderArgs.__new__(OrderArgs)

            __props__.__dict__["components"] = components
            __props__.__dict__["coupon_id"] = coupon_id
            __props__.__dict__["duration"] = duration
            if package_version is None and not opts.urn:
                raise TypeError("Missing required property 'package_version'")
            __props__.__dict__["package_version"] = package_version
            __props__.__dict__["pay_type"] = pay_type
            if pricing_cycle is None and not opts.urn:
                raise TypeError("Missing required property 'pricing_cycle'")
            __props__.__dict__["pricing_cycle"] = pricing_cycle
            if product_code is None and not opts.urn:
                raise TypeError("Missing required property 'product_code'")
            __props__.__dict__["product_code"] = product_code
            __props__.__dict__["quantity"] = quantity
        super(Order, __self__).__init__(
            'alicloud:marketplace/order:Order',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            components: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            coupon_id: Optional[pulumi.Input[str]] = None,
            duration: Optional[pulumi.Input[int]] = None,
            package_version: Optional[pulumi.Input[str]] = None,
            pay_type: Optional[pulumi.Input[str]] = None,
            pricing_cycle: Optional[pulumi.Input[str]] = None,
            product_code: Optional[pulumi.Input[str]] = None,
            quantity: Optional[pulumi.Input[int]] = None) -> 'Order':
        """
        Get an existing Order resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, Any]] components: Service providers customize additional components.
        :param pulumi.Input[str] coupon_id: The coupon id of the market product.
        :param pulumi.Input[int] duration: The number of purchase cycles.
        :param pulumi.Input[str] package_version: The package version of the market product.
        :param pulumi.Input[str] pay_type: Valid values are `PrePaid`, `PostPaid`,System default to `PostPaid`.
        :param pulumi.Input[str] pricing_cycle: The purchase cycle of the product, valid values are `Day`, `Month` and `Year`.
        :param pulumi.Input[str] product_code: The product_code of market place product.
        :param pulumi.Input[int] quantity: The quantity of the market product will be purchased.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OrderState.__new__(_OrderState)

        __props__.__dict__["components"] = components
        __props__.__dict__["coupon_id"] = coupon_id
        __props__.__dict__["duration"] = duration
        __props__.__dict__["package_version"] = package_version
        __props__.__dict__["pay_type"] = pay_type
        __props__.__dict__["pricing_cycle"] = pricing_cycle
        __props__.__dict__["product_code"] = product_code
        __props__.__dict__["quantity"] = quantity
        return Order(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def components(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        Service providers customize additional components.
        """
        return pulumi.get(self, "components")

    @property
    @pulumi.getter(name="couponId")
    def coupon_id(self) -> pulumi.Output[Optional[str]]:
        """
        The coupon id of the market product.
        """
        return pulumi.get(self, "coupon_id")

    @property
    @pulumi.getter
    def duration(self) -> pulumi.Output[Optional[int]]:
        """
        The number of purchase cycles.
        """
        return pulumi.get(self, "duration")

    @property
    @pulumi.getter(name="packageVersion")
    def package_version(self) -> pulumi.Output[str]:
        """
        The package version of the market product.
        """
        return pulumi.get(self, "package_version")

    @property
    @pulumi.getter(name="payType")
    def pay_type(self) -> pulumi.Output[Optional[str]]:
        """
        Valid values are `PrePaid`, `PostPaid`,System default to `PostPaid`.
        """
        return pulumi.get(self, "pay_type")

    @property
    @pulumi.getter(name="pricingCycle")
    def pricing_cycle(self) -> pulumi.Output[str]:
        """
        The purchase cycle of the product, valid values are `Day`, `Month` and `Year`.
        """
        return pulumi.get(self, "pricing_cycle")

    @property
    @pulumi.getter(name="productCode")
    def product_code(self) -> pulumi.Output[str]:
        """
        The product_code of market place product.
        """
        return pulumi.get(self, "product_code")

    @property
    @pulumi.getter
    def quantity(self) -> pulumi.Output[Optional[int]]:
        """
        The quantity of the market product will be purchased.
        """
        return pulumi.get(self, "quantity")

