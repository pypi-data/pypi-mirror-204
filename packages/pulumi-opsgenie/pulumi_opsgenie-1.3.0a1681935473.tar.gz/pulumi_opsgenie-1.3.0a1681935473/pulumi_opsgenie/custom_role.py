# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['CustomRoleArgs', 'CustomRole']

@pulumi.input_type
class CustomRoleArgs:
    def __init__(__self__, *,
                 role_name: pulumi.Input[str],
                 disallowed_rights: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 extended_role: Optional[pulumi.Input[str]] = None,
                 granted_rights: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a CustomRole resource.
        :param pulumi.Input[str] role_name: Name of the custom role.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] disallowed_rights: The rights this role cannot have. For allowed values please refer [User Right Prerequisites](https://docs.opsgenie.com/docs/custom-user-role-api#section-user-right-prerequisites)
        :param pulumi.Input[str] extended_role: The role from which this role has been derived. Allowed Values: "user", "observer", "stakeholder".
        :param pulumi.Input[Sequence[pulumi.Input[str]]] granted_rights: The rights granted to this role. For allowed values please refer [User Right Prerequisites](https://docs.opsgenie.com/docs/custom-user-role-api#section-user-right-prerequisites)
        """
        pulumi.set(__self__, "role_name", role_name)
        if disallowed_rights is not None:
            pulumi.set(__self__, "disallowed_rights", disallowed_rights)
        if extended_role is not None:
            pulumi.set(__self__, "extended_role", extended_role)
        if granted_rights is not None:
            pulumi.set(__self__, "granted_rights", granted_rights)

    @property
    @pulumi.getter(name="roleName")
    def role_name(self) -> pulumi.Input[str]:
        """
        Name of the custom role.
        """
        return pulumi.get(self, "role_name")

    @role_name.setter
    def role_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_name", value)

    @property
    @pulumi.getter(name="disallowedRights")
    def disallowed_rights(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The rights this role cannot have. For allowed values please refer [User Right Prerequisites](https://docs.opsgenie.com/docs/custom-user-role-api#section-user-right-prerequisites)
        """
        return pulumi.get(self, "disallowed_rights")

    @disallowed_rights.setter
    def disallowed_rights(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "disallowed_rights", value)

    @property
    @pulumi.getter(name="extendedRole")
    def extended_role(self) -> Optional[pulumi.Input[str]]:
        """
        The role from which this role has been derived. Allowed Values: "user", "observer", "stakeholder".
        """
        return pulumi.get(self, "extended_role")

    @extended_role.setter
    def extended_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "extended_role", value)

    @property
    @pulumi.getter(name="grantedRights")
    def granted_rights(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The rights granted to this role. For allowed values please refer [User Right Prerequisites](https://docs.opsgenie.com/docs/custom-user-role-api#section-user-right-prerequisites)
        """
        return pulumi.get(self, "granted_rights")

    @granted_rights.setter
    def granted_rights(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "granted_rights", value)


@pulumi.input_type
class _CustomRoleState:
    def __init__(__self__, *,
                 disallowed_rights: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 extended_role: Optional[pulumi.Input[str]] = None,
                 granted_rights: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 role_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering CustomRole resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] disallowed_rights: The rights this role cannot have. For allowed values please refer [User Right Prerequisites](https://docs.opsgenie.com/docs/custom-user-role-api#section-user-right-prerequisites)
        :param pulumi.Input[str] extended_role: The role from which this role has been derived. Allowed Values: "user", "observer", "stakeholder".
        :param pulumi.Input[Sequence[pulumi.Input[str]]] granted_rights: The rights granted to this role. For allowed values please refer [User Right Prerequisites](https://docs.opsgenie.com/docs/custom-user-role-api#section-user-right-prerequisites)
        :param pulumi.Input[str] role_name: Name of the custom role.
        """
        if disallowed_rights is not None:
            pulumi.set(__self__, "disallowed_rights", disallowed_rights)
        if extended_role is not None:
            pulumi.set(__self__, "extended_role", extended_role)
        if granted_rights is not None:
            pulumi.set(__self__, "granted_rights", granted_rights)
        if role_name is not None:
            pulumi.set(__self__, "role_name", role_name)

    @property
    @pulumi.getter(name="disallowedRights")
    def disallowed_rights(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The rights this role cannot have. For allowed values please refer [User Right Prerequisites](https://docs.opsgenie.com/docs/custom-user-role-api#section-user-right-prerequisites)
        """
        return pulumi.get(self, "disallowed_rights")

    @disallowed_rights.setter
    def disallowed_rights(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "disallowed_rights", value)

    @property
    @pulumi.getter(name="extendedRole")
    def extended_role(self) -> Optional[pulumi.Input[str]]:
        """
        The role from which this role has been derived. Allowed Values: "user", "observer", "stakeholder".
        """
        return pulumi.get(self, "extended_role")

    @extended_role.setter
    def extended_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "extended_role", value)

    @property
    @pulumi.getter(name="grantedRights")
    def granted_rights(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The rights granted to this role. For allowed values please refer [User Right Prerequisites](https://docs.opsgenie.com/docs/custom-user-role-api#section-user-right-prerequisites)
        """
        return pulumi.get(self, "granted_rights")

    @granted_rights.setter
    def granted_rights(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "granted_rights", value)

    @property
    @pulumi.getter(name="roleName")
    def role_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the custom role.
        """
        return pulumi.get(self, "role_name")

    @role_name.setter
    def role_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_name", value)


class CustomRole(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 disallowed_rights: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 extended_role: Optional[pulumi.Input[str]] = None,
                 granted_rights: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 role_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages custom user roles within Opsgenie.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_opsgenie as opsgenie

        test = opsgenie.CustomRole("test",
            disallowed_rights=[
                "profile-edit",
                "contacts-edit",
            ],
            extended_role="user",
            granted_rights=["alert-delete"],
            role_name="genierole")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] disallowed_rights: The rights this role cannot have. For allowed values please refer [User Right Prerequisites](https://docs.opsgenie.com/docs/custom-user-role-api#section-user-right-prerequisites)
        :param pulumi.Input[str] extended_role: The role from which this role has been derived. Allowed Values: "user", "observer", "stakeholder".
        :param pulumi.Input[Sequence[pulumi.Input[str]]] granted_rights: The rights granted to this role. For allowed values please refer [User Right Prerequisites](https://docs.opsgenie.com/docs/custom-user-role-api#section-user-right-prerequisites)
        :param pulumi.Input[str] role_name: Name of the custom role.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CustomRoleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages custom user roles within Opsgenie.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_opsgenie as opsgenie

        test = opsgenie.CustomRole("test",
            disallowed_rights=[
                "profile-edit",
                "contacts-edit",
            ],
            extended_role="user",
            granted_rights=["alert-delete"],
            role_name="genierole")
        ```

        :param str resource_name: The name of the resource.
        :param CustomRoleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CustomRoleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 disallowed_rights: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 extended_role: Optional[pulumi.Input[str]] = None,
                 granted_rights: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 role_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CustomRoleArgs.__new__(CustomRoleArgs)

            __props__.__dict__["disallowed_rights"] = disallowed_rights
            __props__.__dict__["extended_role"] = extended_role
            __props__.__dict__["granted_rights"] = granted_rights
            if role_name is None and not opts.urn:
                raise TypeError("Missing required property 'role_name'")
            __props__.__dict__["role_name"] = role_name
        super(CustomRole, __self__).__init__(
            'opsgenie:index/customRole:CustomRole',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            disallowed_rights: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            extended_role: Optional[pulumi.Input[str]] = None,
            granted_rights: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            role_name: Optional[pulumi.Input[str]] = None) -> 'CustomRole':
        """
        Get an existing CustomRole resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] disallowed_rights: The rights this role cannot have. For allowed values please refer [User Right Prerequisites](https://docs.opsgenie.com/docs/custom-user-role-api#section-user-right-prerequisites)
        :param pulumi.Input[str] extended_role: The role from which this role has been derived. Allowed Values: "user", "observer", "stakeholder".
        :param pulumi.Input[Sequence[pulumi.Input[str]]] granted_rights: The rights granted to this role. For allowed values please refer [User Right Prerequisites](https://docs.opsgenie.com/docs/custom-user-role-api#section-user-right-prerequisites)
        :param pulumi.Input[str] role_name: Name of the custom role.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CustomRoleState.__new__(_CustomRoleState)

        __props__.__dict__["disallowed_rights"] = disallowed_rights
        __props__.__dict__["extended_role"] = extended_role
        __props__.__dict__["granted_rights"] = granted_rights
        __props__.__dict__["role_name"] = role_name
        return CustomRole(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="disallowedRights")
    def disallowed_rights(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The rights this role cannot have. For allowed values please refer [User Right Prerequisites](https://docs.opsgenie.com/docs/custom-user-role-api#section-user-right-prerequisites)
        """
        return pulumi.get(self, "disallowed_rights")

    @property
    @pulumi.getter(name="extendedRole")
    def extended_role(self) -> pulumi.Output[Optional[str]]:
        """
        The role from which this role has been derived. Allowed Values: "user", "observer", "stakeholder".
        """
        return pulumi.get(self, "extended_role")

    @property
    @pulumi.getter(name="grantedRights")
    def granted_rights(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The rights granted to this role. For allowed values please refer [User Right Prerequisites](https://docs.opsgenie.com/docs/custom-user-role-api#section-user-right-prerequisites)
        """
        return pulumi.get(self, "granted_rights")

    @property
    @pulumi.getter(name="roleName")
    def role_name(self) -> pulumi.Output[str]:
        """
        Name of the custom role.
        """
        return pulumi.get(self, "role_name")

