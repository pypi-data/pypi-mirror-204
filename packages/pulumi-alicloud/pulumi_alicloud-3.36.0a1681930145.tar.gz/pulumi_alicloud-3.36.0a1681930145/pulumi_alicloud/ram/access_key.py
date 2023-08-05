# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AccessKeyArgs', 'AccessKey']

@pulumi.input_type
class AccessKeyArgs:
    def __init__(__self__, *,
                 pgp_key: Optional[pulumi.Input[str]] = None,
                 secret_file: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AccessKey resource.
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:some_person_that_exists`
        :param pulumi.Input[str] secret_file: The name of file that can save access key id and access key secret. Strongly suggest you to specified it when you creating access key, otherwise, you wouldn't get its secret ever.
        :param pulumi.Input[str] status: Status of access key. It must be `Active` or `Inactive`. Default value is `Active`.
        :param pulumi.Input[str] user_name: Name of the RAM user. This name can have a string of 1 to 64 characters, must contain only alphanumeric characters or hyphens, such as "-",".","_", and must not begin with a hyphen.
        """
        if pgp_key is not None:
            pulumi.set(__self__, "pgp_key", pgp_key)
        if secret_file is not None:
            pulumi.set(__self__, "secret_file", secret_file)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if user_name is not None:
            pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter(name="pgpKey")
    def pgp_key(self) -> Optional[pulumi.Input[str]]:
        """
        Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:some_person_that_exists`
        """
        return pulumi.get(self, "pgp_key")

    @pgp_key.setter
    def pgp_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pgp_key", value)

    @property
    @pulumi.getter(name="secretFile")
    def secret_file(self) -> Optional[pulumi.Input[str]]:
        """
        The name of file that can save access key id and access key secret. Strongly suggest you to specified it when you creating access key, otherwise, you wouldn't get its secret ever.
        """
        return pulumi.get(self, "secret_file")

    @secret_file.setter
    def secret_file(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret_file", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Status of access key. It must be `Active` or `Inactive`. Default value is `Active`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the RAM user. This name can have a string of 1 to 64 characters, must contain only alphanumeric characters or hyphens, such as "-",".","_", and must not begin with a hyphen.
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_name", value)


@pulumi.input_type
class _AccessKeyState:
    def __init__(__self__, *,
                 encrypted_secret: Optional[pulumi.Input[str]] = None,
                 key_fingerprint: Optional[pulumi.Input[str]] = None,
                 pgp_key: Optional[pulumi.Input[str]] = None,
                 secret: Optional[pulumi.Input[str]] = None,
                 secret_file: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AccessKey resources.
        :param pulumi.Input[str] key_fingerprint: The fingerprint of the PGP key used to encrypt the secret
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:some_person_that_exists`
        :param pulumi.Input[str] secret: (Available in 1.98.0+) - The secret access key. Note that this will be written to the state file. 
               If you use this, please protect your backend state file judiciously.
               Alternatively, you may supply a `pgp_key` instead, which will prevent the secret from being stored in plaintext,
               at the cost of preventing the use of the secret key in automation.
        :param pulumi.Input[str] secret_file: The name of file that can save access key id and access key secret. Strongly suggest you to specified it when you creating access key, otherwise, you wouldn't get its secret ever.
        :param pulumi.Input[str] status: Status of access key. It must be `Active` or `Inactive`. Default value is `Active`.
        :param pulumi.Input[str] user_name: Name of the RAM user. This name can have a string of 1 to 64 characters, must contain only alphanumeric characters or hyphens, such as "-",".","_", and must not begin with a hyphen.
        """
        if encrypted_secret is not None:
            pulumi.set(__self__, "encrypted_secret", encrypted_secret)
        if key_fingerprint is not None:
            pulumi.set(__self__, "key_fingerprint", key_fingerprint)
        if pgp_key is not None:
            pulumi.set(__self__, "pgp_key", pgp_key)
        if secret is not None:
            pulumi.set(__self__, "secret", secret)
        if secret_file is not None:
            pulumi.set(__self__, "secret_file", secret_file)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if user_name is not None:
            pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter(name="encryptedSecret")
    def encrypted_secret(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "encrypted_secret")

    @encrypted_secret.setter
    def encrypted_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "encrypted_secret", value)

    @property
    @pulumi.getter(name="keyFingerprint")
    def key_fingerprint(self) -> Optional[pulumi.Input[str]]:
        """
        The fingerprint of the PGP key used to encrypt the secret
        """
        return pulumi.get(self, "key_fingerprint")

    @key_fingerprint.setter
    def key_fingerprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_fingerprint", value)

    @property
    @pulumi.getter(name="pgpKey")
    def pgp_key(self) -> Optional[pulumi.Input[str]]:
        """
        Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:some_person_that_exists`
        """
        return pulumi.get(self, "pgp_key")

    @pgp_key.setter
    def pgp_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pgp_key", value)

    @property
    @pulumi.getter
    def secret(self) -> Optional[pulumi.Input[str]]:
        """
        (Available in 1.98.0+) - The secret access key. Note that this will be written to the state file. 
        If you use this, please protect your backend state file judiciously.
        Alternatively, you may supply a `pgp_key` instead, which will prevent the secret from being stored in plaintext,
        at the cost of preventing the use of the secret key in automation.
        """
        return pulumi.get(self, "secret")

    @secret.setter
    def secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret", value)

    @property
    @pulumi.getter(name="secretFile")
    def secret_file(self) -> Optional[pulumi.Input[str]]:
        """
        The name of file that can save access key id and access key secret. Strongly suggest you to specified it when you creating access key, otherwise, you wouldn't get its secret ever.
        """
        return pulumi.get(self, "secret_file")

    @secret_file.setter
    def secret_file(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret_file", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Status of access key. It must be `Active` or `Inactive`. Default value is `Active`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the RAM user. This name can have a string of 1 to 64 characters, must contain only alphanumeric characters or hyphens, such as "-",".","_", and must not begin with a hyphen.
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_name", value)


class AccessKey(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 pgp_key: Optional[pulumi.Input[str]] = None,
                 secret_file: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a RAM User access key resource.

        > **NOTE:**  You should set the `secret_file` if you want to get the access key.

        > **NOTE:**  From version 1.98.0, if not set `pgp_key`, the resource will output the access key secret to field `secret` and please protect your backend state file judiciously

        ## Example Usage

        Output the secret to a file.
        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        # Create a new RAM access key for user.
        user = alicloud.ram.User("user",
            display_name="user_display_name",
            mobile="86-18688888888",
            email="hello.uuu@aaa.com",
            comments="yoyoyo",
            force=True)
        ak = alicloud.ram.AccessKey("ak",
            user_name=user.name,
            secret_file="/xxx/xxx/xxx.txt")
        ```

        Using `pgp_key` to encrypt the secret.
        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        # Create a new RAM access key for user.
        user = alicloud.ram.User("user",
            display_name="user_display_name",
            mobile="86-18688888888",
            email="hello.uuu@aaa.com",
            comments="yoyoyo",
            force=True)
        encrypt = alicloud.ram.AccessKey("encrypt",
            user_name=user.name,
            pgp_key="keybase:some_person_that_exists")
        pulumi.export("secret", encrypt.encrypted_secret)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:some_person_that_exists`
        :param pulumi.Input[str] secret_file: The name of file that can save access key id and access key secret. Strongly suggest you to specified it when you creating access key, otherwise, you wouldn't get its secret ever.
        :param pulumi.Input[str] status: Status of access key. It must be `Active` or `Inactive`. Default value is `Active`.
        :param pulumi.Input[str] user_name: Name of the RAM user. This name can have a string of 1 to 64 characters, must contain only alphanumeric characters or hyphens, such as "-",".","_", and must not begin with a hyphen.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[AccessKeyArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a RAM User access key resource.

        > **NOTE:**  You should set the `secret_file` if you want to get the access key.

        > **NOTE:**  From version 1.98.0, if not set `pgp_key`, the resource will output the access key secret to field `secret` and please protect your backend state file judiciously

        ## Example Usage

        Output the secret to a file.
        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        # Create a new RAM access key for user.
        user = alicloud.ram.User("user",
            display_name="user_display_name",
            mobile="86-18688888888",
            email="hello.uuu@aaa.com",
            comments="yoyoyo",
            force=True)
        ak = alicloud.ram.AccessKey("ak",
            user_name=user.name,
            secret_file="/xxx/xxx/xxx.txt")
        ```

        Using `pgp_key` to encrypt the secret.
        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        # Create a new RAM access key for user.
        user = alicloud.ram.User("user",
            display_name="user_display_name",
            mobile="86-18688888888",
            email="hello.uuu@aaa.com",
            comments="yoyoyo",
            force=True)
        encrypt = alicloud.ram.AccessKey("encrypt",
            user_name=user.name,
            pgp_key="keybase:some_person_that_exists")
        pulumi.export("secret", encrypt.encrypted_secret)
        ```

        :param str resource_name: The name of the resource.
        :param AccessKeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccessKeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 pgp_key: Optional[pulumi.Input[str]] = None,
                 secret_file: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccessKeyArgs.__new__(AccessKeyArgs)

            __props__.__dict__["pgp_key"] = pgp_key
            __props__.__dict__["secret_file"] = secret_file
            __props__.__dict__["status"] = status
            __props__.__dict__["user_name"] = user_name
            __props__.__dict__["encrypted_secret"] = None
            __props__.__dict__["key_fingerprint"] = None
            __props__.__dict__["secret"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["secret"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(AccessKey, __self__).__init__(
            'alicloud:ram/accessKey:AccessKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            encrypted_secret: Optional[pulumi.Input[str]] = None,
            key_fingerprint: Optional[pulumi.Input[str]] = None,
            pgp_key: Optional[pulumi.Input[str]] = None,
            secret: Optional[pulumi.Input[str]] = None,
            secret_file: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            user_name: Optional[pulumi.Input[str]] = None) -> 'AccessKey':
        """
        Get an existing AccessKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] key_fingerprint: The fingerprint of the PGP key used to encrypt the secret
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:some_person_that_exists`
        :param pulumi.Input[str] secret: (Available in 1.98.0+) - The secret access key. Note that this will be written to the state file. 
               If you use this, please protect your backend state file judiciously.
               Alternatively, you may supply a `pgp_key` instead, which will prevent the secret from being stored in plaintext,
               at the cost of preventing the use of the secret key in automation.
        :param pulumi.Input[str] secret_file: The name of file that can save access key id and access key secret. Strongly suggest you to specified it when you creating access key, otherwise, you wouldn't get its secret ever.
        :param pulumi.Input[str] status: Status of access key. It must be `Active` or `Inactive`. Default value is `Active`.
        :param pulumi.Input[str] user_name: Name of the RAM user. This name can have a string of 1 to 64 characters, must contain only alphanumeric characters or hyphens, such as "-",".","_", and must not begin with a hyphen.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AccessKeyState.__new__(_AccessKeyState)

        __props__.__dict__["encrypted_secret"] = encrypted_secret
        __props__.__dict__["key_fingerprint"] = key_fingerprint
        __props__.__dict__["pgp_key"] = pgp_key
        __props__.__dict__["secret"] = secret
        __props__.__dict__["secret_file"] = secret_file
        __props__.__dict__["status"] = status
        __props__.__dict__["user_name"] = user_name
        return AccessKey(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="encryptedSecret")
    def encrypted_secret(self) -> pulumi.Output[str]:
        return pulumi.get(self, "encrypted_secret")

    @property
    @pulumi.getter(name="keyFingerprint")
    def key_fingerprint(self) -> pulumi.Output[str]:
        """
        The fingerprint of the PGP key used to encrypt the secret
        """
        return pulumi.get(self, "key_fingerprint")

    @property
    @pulumi.getter(name="pgpKey")
    def pgp_key(self) -> pulumi.Output[Optional[str]]:
        """
        Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:some_person_that_exists`
        """
        return pulumi.get(self, "pgp_key")

    @property
    @pulumi.getter
    def secret(self) -> pulumi.Output[str]:
        """
        (Available in 1.98.0+) - The secret access key. Note that this will be written to the state file. 
        If you use this, please protect your backend state file judiciously.
        Alternatively, you may supply a `pgp_key` instead, which will prevent the secret from being stored in plaintext,
        at the cost of preventing the use of the secret key in automation.
        """
        return pulumi.get(self, "secret")

    @property
    @pulumi.getter(name="secretFile")
    def secret_file(self) -> pulumi.Output[Optional[str]]:
        """
        The name of file that can save access key id and access key secret. Strongly suggest you to specified it when you creating access key, otherwise, you wouldn't get its secret ever.
        """
        return pulumi.get(self, "secret_file")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        Status of access key. It must be `Active` or `Inactive`. Default value is `Active`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> pulumi.Output[Optional[str]]:
        """
        Name of the RAM user. This name can have a string of 1 to 64 characters, must contain only alphanumeric characters or hyphens, such as "-",".","_", and must not begin with a hyphen.
        """
        return pulumi.get(self, "user_name")

