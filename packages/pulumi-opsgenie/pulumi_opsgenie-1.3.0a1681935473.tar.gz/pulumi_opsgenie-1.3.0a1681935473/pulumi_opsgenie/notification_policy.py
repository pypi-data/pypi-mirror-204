# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['NotificationPolicyArgs', 'NotificationPolicy']

@pulumi.input_type
class NotificationPolicyArgs:
    def __init__(__self__, *,
                 filters: pulumi.Input[Sequence[pulumi.Input['NotificationPolicyFilterArgs']]],
                 team_id: pulumi.Input[str],
                 auto_close_actions: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoCloseActionArgs']]]] = None,
                 auto_restart_actions: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoRestartActionArgs']]]] = None,
                 de_duplication_actions: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDeDuplicationActionArgs']]]] = None,
                 delay_actions: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDelayActionArgs']]]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_description: Optional[pulumi.Input[str]] = None,
                 suppress: Optional[pulumi.Input[bool]] = None,
                 time_restrictions: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyTimeRestrictionArgs']]]] = None):
        """
        The set of arguments for constructing a NotificationPolicy resource.
        :param pulumi.Input[Sequence[pulumi.Input['NotificationPolicyFilterArgs']]] filters: A notification filter which will be applied. This filter can be empty: `filter {}` - this means `match-all`. This is a block, structure is documented below.
        :param pulumi.Input[str] team_id: Id of team that this policy belons to.
        :param pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoCloseActionArgs']]] auto_close_actions: Auto Restart Action of the policy. This is a block, structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoRestartActionArgs']]] auto_restart_actions: Auto Restart Action of the policy. This is a block, structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDeDuplicationActionArgs']]] de_duplication_actions: Deduplication Action of the policy. This is a block, structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDelayActionArgs']]] delay_actions: Delay notifications. This is a block, structure is documented below.
        :param pulumi.Input[bool] enabled: If policy should be enabled. Default: `true`
        :param pulumi.Input[str] name: Name of the notification policy
        :param pulumi.Input[str] policy_description: Description of the policy. This can be max 512 characters.
        :param pulumi.Input[bool] suppress: Suppress value of the policy. Values are: `true`, `false`. Default: `false`
        :param pulumi.Input[Sequence[pulumi.Input['NotificationPolicyTimeRestrictionArgs']]] time_restrictions: Time restrictions specified in this field must be met for this policy to work. This is a block, structure is documented below.
        """
        pulumi.set(__self__, "filters", filters)
        pulumi.set(__self__, "team_id", team_id)
        if auto_close_actions is not None:
            pulumi.set(__self__, "auto_close_actions", auto_close_actions)
        if auto_restart_actions is not None:
            pulumi.set(__self__, "auto_restart_actions", auto_restart_actions)
        if de_duplication_actions is not None:
            pulumi.set(__self__, "de_duplication_actions", de_duplication_actions)
        if delay_actions is not None:
            pulumi.set(__self__, "delay_actions", delay_actions)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if policy_description is not None:
            pulumi.set(__self__, "policy_description", policy_description)
        if suppress is not None:
            pulumi.set(__self__, "suppress", suppress)
        if time_restrictions is not None:
            pulumi.set(__self__, "time_restrictions", time_restrictions)

    @property
    @pulumi.getter
    def filters(self) -> pulumi.Input[Sequence[pulumi.Input['NotificationPolicyFilterArgs']]]:
        """
        A notification filter which will be applied. This filter can be empty: `filter {}` - this means `match-all`. This is a block, structure is documented below.
        """
        return pulumi.get(self, "filters")

    @filters.setter
    def filters(self, value: pulumi.Input[Sequence[pulumi.Input['NotificationPolicyFilterArgs']]]):
        pulumi.set(self, "filters", value)

    @property
    @pulumi.getter(name="teamId")
    def team_id(self) -> pulumi.Input[str]:
        """
        Id of team that this policy belons to.
        """
        return pulumi.get(self, "team_id")

    @team_id.setter
    def team_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "team_id", value)

    @property
    @pulumi.getter(name="autoCloseActions")
    def auto_close_actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoCloseActionArgs']]]]:
        """
        Auto Restart Action of the policy. This is a block, structure is documented below.
        """
        return pulumi.get(self, "auto_close_actions")

    @auto_close_actions.setter
    def auto_close_actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoCloseActionArgs']]]]):
        pulumi.set(self, "auto_close_actions", value)

    @property
    @pulumi.getter(name="autoRestartActions")
    def auto_restart_actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoRestartActionArgs']]]]:
        """
        Auto Restart Action of the policy. This is a block, structure is documented below.
        """
        return pulumi.get(self, "auto_restart_actions")

    @auto_restart_actions.setter
    def auto_restart_actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoRestartActionArgs']]]]):
        pulumi.set(self, "auto_restart_actions", value)

    @property
    @pulumi.getter(name="deDuplicationActions")
    def de_duplication_actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDeDuplicationActionArgs']]]]:
        """
        Deduplication Action of the policy. This is a block, structure is documented below.
        """
        return pulumi.get(self, "de_duplication_actions")

    @de_duplication_actions.setter
    def de_duplication_actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDeDuplicationActionArgs']]]]):
        pulumi.set(self, "de_duplication_actions", value)

    @property
    @pulumi.getter(name="delayActions")
    def delay_actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDelayActionArgs']]]]:
        """
        Delay notifications. This is a block, structure is documented below.
        """
        return pulumi.get(self, "delay_actions")

    @delay_actions.setter
    def delay_actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDelayActionArgs']]]]):
        pulumi.set(self, "delay_actions", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        If policy should be enabled. Default: `true`
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the notification policy
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="policyDescription")
    def policy_description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the policy. This can be max 512 characters.
        """
        return pulumi.get(self, "policy_description")

    @policy_description.setter
    def policy_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_description", value)

    @property
    @pulumi.getter
    def suppress(self) -> Optional[pulumi.Input[bool]]:
        """
        Suppress value of the policy. Values are: `true`, `false`. Default: `false`
        """
        return pulumi.get(self, "suppress")

    @suppress.setter
    def suppress(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "suppress", value)

    @property
    @pulumi.getter(name="timeRestrictions")
    def time_restrictions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyTimeRestrictionArgs']]]]:
        """
        Time restrictions specified in this field must be met for this policy to work. This is a block, structure is documented below.
        """
        return pulumi.get(self, "time_restrictions")

    @time_restrictions.setter
    def time_restrictions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyTimeRestrictionArgs']]]]):
        pulumi.set(self, "time_restrictions", value)


@pulumi.input_type
class _NotificationPolicyState:
    def __init__(__self__, *,
                 auto_close_actions: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoCloseActionArgs']]]] = None,
                 auto_restart_actions: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoRestartActionArgs']]]] = None,
                 de_duplication_actions: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDeDuplicationActionArgs']]]] = None,
                 delay_actions: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDelayActionArgs']]]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 filters: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyFilterArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_description: Optional[pulumi.Input[str]] = None,
                 suppress: Optional[pulumi.Input[bool]] = None,
                 team_id: Optional[pulumi.Input[str]] = None,
                 time_restrictions: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyTimeRestrictionArgs']]]] = None):
        """
        Input properties used for looking up and filtering NotificationPolicy resources.
        :param pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoCloseActionArgs']]] auto_close_actions: Auto Restart Action of the policy. This is a block, structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoRestartActionArgs']]] auto_restart_actions: Auto Restart Action of the policy. This is a block, structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDeDuplicationActionArgs']]] de_duplication_actions: Deduplication Action of the policy. This is a block, structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDelayActionArgs']]] delay_actions: Delay notifications. This is a block, structure is documented below.
        :param pulumi.Input[bool] enabled: If policy should be enabled. Default: `true`
        :param pulumi.Input[Sequence[pulumi.Input['NotificationPolicyFilterArgs']]] filters: A notification filter which will be applied. This filter can be empty: `filter {}` - this means `match-all`. This is a block, structure is documented below.
        :param pulumi.Input[str] name: Name of the notification policy
        :param pulumi.Input[str] policy_description: Description of the policy. This can be max 512 characters.
        :param pulumi.Input[bool] suppress: Suppress value of the policy. Values are: `true`, `false`. Default: `false`
        :param pulumi.Input[str] team_id: Id of team that this policy belons to.
        :param pulumi.Input[Sequence[pulumi.Input['NotificationPolicyTimeRestrictionArgs']]] time_restrictions: Time restrictions specified in this field must be met for this policy to work. This is a block, structure is documented below.
        """
        if auto_close_actions is not None:
            pulumi.set(__self__, "auto_close_actions", auto_close_actions)
        if auto_restart_actions is not None:
            pulumi.set(__self__, "auto_restart_actions", auto_restart_actions)
        if de_duplication_actions is not None:
            pulumi.set(__self__, "de_duplication_actions", de_duplication_actions)
        if delay_actions is not None:
            pulumi.set(__self__, "delay_actions", delay_actions)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if filters is not None:
            pulumi.set(__self__, "filters", filters)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if policy_description is not None:
            pulumi.set(__self__, "policy_description", policy_description)
        if suppress is not None:
            pulumi.set(__self__, "suppress", suppress)
        if team_id is not None:
            pulumi.set(__self__, "team_id", team_id)
        if time_restrictions is not None:
            pulumi.set(__self__, "time_restrictions", time_restrictions)

    @property
    @pulumi.getter(name="autoCloseActions")
    def auto_close_actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoCloseActionArgs']]]]:
        """
        Auto Restart Action of the policy. This is a block, structure is documented below.
        """
        return pulumi.get(self, "auto_close_actions")

    @auto_close_actions.setter
    def auto_close_actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoCloseActionArgs']]]]):
        pulumi.set(self, "auto_close_actions", value)

    @property
    @pulumi.getter(name="autoRestartActions")
    def auto_restart_actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoRestartActionArgs']]]]:
        """
        Auto Restart Action of the policy. This is a block, structure is documented below.
        """
        return pulumi.get(self, "auto_restart_actions")

    @auto_restart_actions.setter
    def auto_restart_actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyAutoRestartActionArgs']]]]):
        pulumi.set(self, "auto_restart_actions", value)

    @property
    @pulumi.getter(name="deDuplicationActions")
    def de_duplication_actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDeDuplicationActionArgs']]]]:
        """
        Deduplication Action of the policy. This is a block, structure is documented below.
        """
        return pulumi.get(self, "de_duplication_actions")

    @de_duplication_actions.setter
    def de_duplication_actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDeDuplicationActionArgs']]]]):
        pulumi.set(self, "de_duplication_actions", value)

    @property
    @pulumi.getter(name="delayActions")
    def delay_actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDelayActionArgs']]]]:
        """
        Delay notifications. This is a block, structure is documented below.
        """
        return pulumi.get(self, "delay_actions")

    @delay_actions.setter
    def delay_actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyDelayActionArgs']]]]):
        pulumi.set(self, "delay_actions", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        If policy should be enabled. Default: `true`
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def filters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyFilterArgs']]]]:
        """
        A notification filter which will be applied. This filter can be empty: `filter {}` - this means `match-all`. This is a block, structure is documented below.
        """
        return pulumi.get(self, "filters")

    @filters.setter
    def filters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyFilterArgs']]]]):
        pulumi.set(self, "filters", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the notification policy
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="policyDescription")
    def policy_description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the policy. This can be max 512 characters.
        """
        return pulumi.get(self, "policy_description")

    @policy_description.setter
    def policy_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_description", value)

    @property
    @pulumi.getter
    def suppress(self) -> Optional[pulumi.Input[bool]]:
        """
        Suppress value of the policy. Values are: `true`, `false`. Default: `false`
        """
        return pulumi.get(self, "suppress")

    @suppress.setter
    def suppress(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "suppress", value)

    @property
    @pulumi.getter(name="teamId")
    def team_id(self) -> Optional[pulumi.Input[str]]:
        """
        Id of team that this policy belons to.
        """
        return pulumi.get(self, "team_id")

    @team_id.setter
    def team_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "team_id", value)

    @property
    @pulumi.getter(name="timeRestrictions")
    def time_restrictions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyTimeRestrictionArgs']]]]:
        """
        Time restrictions specified in this field must be met for this policy to work. This is a block, structure is documented below.
        """
        return pulumi.get(self, "time_restrictions")

    @time_restrictions.setter
    def time_restrictions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NotificationPolicyTimeRestrictionArgs']]]]):
        pulumi.set(self, "time_restrictions", value)


class NotificationPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_close_actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyAutoCloseActionArgs']]]]] = None,
                 auto_restart_actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyAutoRestartActionArgs']]]]] = None,
                 de_duplication_actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyDeDuplicationActionArgs']]]]] = None,
                 delay_actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyDelayActionArgs']]]]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 filters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyFilterArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_description: Optional[pulumi.Input[str]] = None,
                 suppress: Optional[pulumi.Input[bool]] = None,
                 team_id: Optional[pulumi.Input[str]] = None,
                 time_restrictions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyTimeRestrictionArgs']]]]] = None,
                 __props__=None):
        """
        Manages a Notification Policy within Opsgenie.

        ## Import

        Notification policies can be imported using the `team_id` and `notification_policy_id`, e.g.

        ```sh
         $ pulumi import opsgenie:index/notificationPolicy:NotificationPolicy test team_id/notification_policy_id`
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyAutoCloseActionArgs']]]] auto_close_actions: Auto Restart Action of the policy. This is a block, structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyAutoRestartActionArgs']]]] auto_restart_actions: Auto Restart Action of the policy. This is a block, structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyDeDuplicationActionArgs']]]] de_duplication_actions: Deduplication Action of the policy. This is a block, structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyDelayActionArgs']]]] delay_actions: Delay notifications. This is a block, structure is documented below.
        :param pulumi.Input[bool] enabled: If policy should be enabled. Default: `true`
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyFilterArgs']]]] filters: A notification filter which will be applied. This filter can be empty: `filter {}` - this means `match-all`. This is a block, structure is documented below.
        :param pulumi.Input[str] name: Name of the notification policy
        :param pulumi.Input[str] policy_description: Description of the policy. This can be max 512 characters.
        :param pulumi.Input[bool] suppress: Suppress value of the policy. Values are: `true`, `false`. Default: `false`
        :param pulumi.Input[str] team_id: Id of team that this policy belons to.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyTimeRestrictionArgs']]]] time_restrictions: Time restrictions specified in this field must be met for this policy to work. This is a block, structure is documented below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NotificationPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Notification Policy within Opsgenie.

        ## Import

        Notification policies can be imported using the `team_id` and `notification_policy_id`, e.g.

        ```sh
         $ pulumi import opsgenie:index/notificationPolicy:NotificationPolicy test team_id/notification_policy_id`
        ```

        :param str resource_name: The name of the resource.
        :param NotificationPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NotificationPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_close_actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyAutoCloseActionArgs']]]]] = None,
                 auto_restart_actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyAutoRestartActionArgs']]]]] = None,
                 de_duplication_actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyDeDuplicationActionArgs']]]]] = None,
                 delay_actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyDelayActionArgs']]]]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 filters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyFilterArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_description: Optional[pulumi.Input[str]] = None,
                 suppress: Optional[pulumi.Input[bool]] = None,
                 team_id: Optional[pulumi.Input[str]] = None,
                 time_restrictions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyTimeRestrictionArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NotificationPolicyArgs.__new__(NotificationPolicyArgs)

            __props__.__dict__["auto_close_actions"] = auto_close_actions
            __props__.__dict__["auto_restart_actions"] = auto_restart_actions
            __props__.__dict__["de_duplication_actions"] = de_duplication_actions
            __props__.__dict__["delay_actions"] = delay_actions
            __props__.__dict__["enabled"] = enabled
            if filters is None and not opts.urn:
                raise TypeError("Missing required property 'filters'")
            __props__.__dict__["filters"] = filters
            __props__.__dict__["name"] = name
            __props__.__dict__["policy_description"] = policy_description
            __props__.__dict__["suppress"] = suppress
            if team_id is None and not opts.urn:
                raise TypeError("Missing required property 'team_id'")
            __props__.__dict__["team_id"] = team_id
            __props__.__dict__["time_restrictions"] = time_restrictions
        super(NotificationPolicy, __self__).__init__(
            'opsgenie:index/notificationPolicy:NotificationPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            auto_close_actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyAutoCloseActionArgs']]]]] = None,
            auto_restart_actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyAutoRestartActionArgs']]]]] = None,
            de_duplication_actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyDeDuplicationActionArgs']]]]] = None,
            delay_actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyDelayActionArgs']]]]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            filters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyFilterArgs']]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            policy_description: Optional[pulumi.Input[str]] = None,
            suppress: Optional[pulumi.Input[bool]] = None,
            team_id: Optional[pulumi.Input[str]] = None,
            time_restrictions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyTimeRestrictionArgs']]]]] = None) -> 'NotificationPolicy':
        """
        Get an existing NotificationPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyAutoCloseActionArgs']]]] auto_close_actions: Auto Restart Action of the policy. This is a block, structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyAutoRestartActionArgs']]]] auto_restart_actions: Auto Restart Action of the policy. This is a block, structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyDeDuplicationActionArgs']]]] de_duplication_actions: Deduplication Action of the policy. This is a block, structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyDelayActionArgs']]]] delay_actions: Delay notifications. This is a block, structure is documented below.
        :param pulumi.Input[bool] enabled: If policy should be enabled. Default: `true`
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyFilterArgs']]]] filters: A notification filter which will be applied. This filter can be empty: `filter {}` - this means `match-all`. This is a block, structure is documented below.
        :param pulumi.Input[str] name: Name of the notification policy
        :param pulumi.Input[str] policy_description: Description of the policy. This can be max 512 characters.
        :param pulumi.Input[bool] suppress: Suppress value of the policy. Values are: `true`, `false`. Default: `false`
        :param pulumi.Input[str] team_id: Id of team that this policy belons to.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NotificationPolicyTimeRestrictionArgs']]]] time_restrictions: Time restrictions specified in this field must be met for this policy to work. This is a block, structure is documented below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NotificationPolicyState.__new__(_NotificationPolicyState)

        __props__.__dict__["auto_close_actions"] = auto_close_actions
        __props__.__dict__["auto_restart_actions"] = auto_restart_actions
        __props__.__dict__["de_duplication_actions"] = de_duplication_actions
        __props__.__dict__["delay_actions"] = delay_actions
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["filters"] = filters
        __props__.__dict__["name"] = name
        __props__.__dict__["policy_description"] = policy_description
        __props__.__dict__["suppress"] = suppress
        __props__.__dict__["team_id"] = team_id
        __props__.__dict__["time_restrictions"] = time_restrictions
        return NotificationPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="autoCloseActions")
    def auto_close_actions(self) -> pulumi.Output[Optional[Sequence['outputs.NotificationPolicyAutoCloseAction']]]:
        """
        Auto Restart Action of the policy. This is a block, structure is documented below.
        """
        return pulumi.get(self, "auto_close_actions")

    @property
    @pulumi.getter(name="autoRestartActions")
    def auto_restart_actions(self) -> pulumi.Output[Optional[Sequence['outputs.NotificationPolicyAutoRestartAction']]]:
        """
        Auto Restart Action of the policy. This is a block, structure is documented below.
        """
        return pulumi.get(self, "auto_restart_actions")

    @property
    @pulumi.getter(name="deDuplicationActions")
    def de_duplication_actions(self) -> pulumi.Output[Optional[Sequence['outputs.NotificationPolicyDeDuplicationAction']]]:
        """
        Deduplication Action of the policy. This is a block, structure is documented below.
        """
        return pulumi.get(self, "de_duplication_actions")

    @property
    @pulumi.getter(name="delayActions")
    def delay_actions(self) -> pulumi.Output[Optional[Sequence['outputs.NotificationPolicyDelayAction']]]:
        """
        Delay notifications. This is a block, structure is documented below.
        """
        return pulumi.get(self, "delay_actions")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        If policy should be enabled. Default: `true`
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def filters(self) -> pulumi.Output[Sequence['outputs.NotificationPolicyFilter']]:
        """
        A notification filter which will be applied. This filter can be empty: `filter {}` - this means `match-all`. This is a block, structure is documented below.
        """
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the notification policy
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="policyDescription")
    def policy_description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the policy. This can be max 512 characters.
        """
        return pulumi.get(self, "policy_description")

    @property
    @pulumi.getter
    def suppress(self) -> pulumi.Output[Optional[bool]]:
        """
        Suppress value of the policy. Values are: `true`, `false`. Default: `false`
        """
        return pulumi.get(self, "suppress")

    @property
    @pulumi.getter(name="teamId")
    def team_id(self) -> pulumi.Output[str]:
        """
        Id of team that this policy belons to.
        """
        return pulumi.get(self, "team_id")

    @property
    @pulumi.getter(name="timeRestrictions")
    def time_restrictions(self) -> pulumi.Output[Optional[Sequence['outputs.NotificationPolicyTimeRestriction']]]:
        """
        Time restrictions specified in this field must be met for this policy to work. This is a block, structure is documented below.
        """
        return pulumi.get(self, "time_restrictions")

