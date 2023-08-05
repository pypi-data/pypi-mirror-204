# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['UserContactArgs', 'UserContact']

@pulumi.input_type
class UserContactArgs:
    def __init__(__self__, *,
                 method: pulumi.Input[str],
                 to: pulumi.Input[str],
                 username: pulumi.Input[str],
                 enabled: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a UserContact resource.
        :param pulumi.Input[str] method: This parameter is the contact method of user and should be one of email, sms or voice. Please note that adding mobile is not supported from API.
        :param pulumi.Input[str] to: to field is the address of given method.
        :param pulumi.Input[str] username: The username for contact.(reference)
        :param pulumi.Input[bool] enabled: Enable contact of the user in OpsGenie. Default value is true.
        """
        pulumi.set(__self__, "method", method)
        pulumi.set(__self__, "to", to)
        pulumi.set(__self__, "username", username)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)

    @property
    @pulumi.getter
    def method(self) -> pulumi.Input[str]:
        """
        This parameter is the contact method of user and should be one of email, sms or voice. Please note that adding mobile is not supported from API.
        """
        return pulumi.get(self, "method")

    @method.setter
    def method(self, value: pulumi.Input[str]):
        pulumi.set(self, "method", value)

    @property
    @pulumi.getter
    def to(self) -> pulumi.Input[str]:
        """
        to field is the address of given method.
        """
        return pulumi.get(self, "to")

    @to.setter
    def to(self, value: pulumi.Input[str]):
        pulumi.set(self, "to", value)

    @property
    @pulumi.getter
    def username(self) -> pulumi.Input[str]:
        """
        The username for contact.(reference)
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: pulumi.Input[str]):
        pulumi.set(self, "username", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable contact of the user in OpsGenie. Default value is true.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)


@pulumi.input_type
class _UserContactState:
    def __init__(__self__, *,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 method: Optional[pulumi.Input[str]] = None,
                 to: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering UserContact resources.
        :param pulumi.Input[bool] enabled: Enable contact of the user in OpsGenie. Default value is true.
        :param pulumi.Input[str] method: This parameter is the contact method of user and should be one of email, sms or voice. Please note that adding mobile is not supported from API.
        :param pulumi.Input[str] to: to field is the address of given method.
        :param pulumi.Input[str] username: The username for contact.(reference)
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if method is not None:
            pulumi.set(__self__, "method", method)
        if to is not None:
            pulumi.set(__self__, "to", to)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable contact of the user in OpsGenie. Default value is true.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def method(self) -> Optional[pulumi.Input[str]]:
        """
        This parameter is the contact method of user and should be one of email, sms or voice. Please note that adding mobile is not supported from API.
        """
        return pulumi.get(self, "method")

    @method.setter
    def method(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "method", value)

    @property
    @pulumi.getter
    def to(self) -> Optional[pulumi.Input[str]]:
        """
        to field is the address of given method.
        """
        return pulumi.get(self, "to")

    @to.setter
    def to(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "to", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        The username for contact.(reference)
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


class UserContact(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 method: Optional[pulumi.Input[str]] = None,
                 to: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a User Contact.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_opsgenie as opsgenie

        sms = opsgenie.UserContact("sms",
            method="sms",
            to="39-123",
            username=opsgenie_user["exampleuser"]["username"])
        email = opsgenie.UserContact("email",
            method="email",
            to="fahri@opsgenie.com",
            username=opsgenie_user["exampleuser"]["username"])
        voice = opsgenie.UserContact("voice",
            method="voice",
            to="39-123",
            username=opsgenie_user["exampleuser"]["username"])
        ```

        ## Import

        Users can be imported using the `username/contact_id`, e.g.

        ```sh
         $ pulumi import opsgenie:index/userContact:UserContact testcontact username/contact_id`
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enabled: Enable contact of the user in OpsGenie. Default value is true.
        :param pulumi.Input[str] method: This parameter is the contact method of user and should be one of email, sms or voice. Please note that adding mobile is not supported from API.
        :param pulumi.Input[str] to: to field is the address of given method.
        :param pulumi.Input[str] username: The username for contact.(reference)
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserContactArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a User Contact.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_opsgenie as opsgenie

        sms = opsgenie.UserContact("sms",
            method="sms",
            to="39-123",
            username=opsgenie_user["exampleuser"]["username"])
        email = opsgenie.UserContact("email",
            method="email",
            to="fahri@opsgenie.com",
            username=opsgenie_user["exampleuser"]["username"])
        voice = opsgenie.UserContact("voice",
            method="voice",
            to="39-123",
            username=opsgenie_user["exampleuser"]["username"])
        ```

        ## Import

        Users can be imported using the `username/contact_id`, e.g.

        ```sh
         $ pulumi import opsgenie:index/userContact:UserContact testcontact username/contact_id`
        ```

        :param str resource_name: The name of the resource.
        :param UserContactArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserContactArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 method: Optional[pulumi.Input[str]] = None,
                 to: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserContactArgs.__new__(UserContactArgs)

            __props__.__dict__["enabled"] = enabled
            if method is None and not opts.urn:
                raise TypeError("Missing required property 'method'")
            __props__.__dict__["method"] = method
            if to is None and not opts.urn:
                raise TypeError("Missing required property 'to'")
            __props__.__dict__["to"] = to
            if username is None and not opts.urn:
                raise TypeError("Missing required property 'username'")
            __props__.__dict__["username"] = username
        super(UserContact, __self__).__init__(
            'opsgenie:index/userContact:UserContact',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            method: Optional[pulumi.Input[str]] = None,
            to: Optional[pulumi.Input[str]] = None,
            username: Optional[pulumi.Input[str]] = None) -> 'UserContact':
        """
        Get an existing UserContact resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enabled: Enable contact of the user in OpsGenie. Default value is true.
        :param pulumi.Input[str] method: This parameter is the contact method of user and should be one of email, sms or voice. Please note that adding mobile is not supported from API.
        :param pulumi.Input[str] to: to field is the address of given method.
        :param pulumi.Input[str] username: The username for contact.(reference)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserContactState.__new__(_UserContactState)

        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["method"] = method
        __props__.__dict__["to"] = to
        __props__.__dict__["username"] = username
        return UserContact(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable contact of the user in OpsGenie. Default value is true.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def method(self) -> pulumi.Output[str]:
        """
        This parameter is the contact method of user and should be one of email, sms or voice. Please note that adding mobile is not supported from API.
        """
        return pulumi.get(self, "method")

    @property
    @pulumi.getter
    def to(self) -> pulumi.Output[str]:
        """
        to field is the address of given method.
        """
        return pulumi.get(self, "to")

    @property
    @pulumi.getter
    def username(self) -> pulumi.Output[str]:
        """
        The username for contact.(reference)
        """
        return pulumi.get(self, "username")

