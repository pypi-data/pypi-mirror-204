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

__all__ = [
    'GetMetricsPolicyResult',
    'AwaitableGetMetricsPolicyResult',
    'get_metrics_policy',
]

@pulumi.output_type
class GetMetricsPolicyResult:
    """
    A collection of values returned by getMetricsPolicy.
    """
    def __init__(__self__, customer=None, id=None, policy_rules=None, updated_epoch_millis=None, updater_id=None):
        if customer and not isinstance(customer, str):
            raise TypeError("Expected argument 'customer' to be a str")
        pulumi.set(__self__, "customer", customer)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if policy_rules and not isinstance(policy_rules, list):
            raise TypeError("Expected argument 'policy_rules' to be a list")
        pulumi.set(__self__, "policy_rules", policy_rules)
        if updated_epoch_millis and not isinstance(updated_epoch_millis, int):
            raise TypeError("Expected argument 'updated_epoch_millis' to be a int")
        pulumi.set(__self__, "updated_epoch_millis", updated_epoch_millis)
        if updater_id and not isinstance(updater_id, str):
            raise TypeError("Expected argument 'updater_id' to be a str")
        pulumi.set(__self__, "updater_id", updater_id)

    @property
    @pulumi.getter
    def customer(self) -> str:
        return pulumi.get(self, "customer")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="policyRules")
    def policy_rules(self) -> Sequence['outputs.GetMetricsPolicyPolicyRuleResult']:
        return pulumi.get(self, "policy_rules")

    @property
    @pulumi.getter(name="updatedEpochMillis")
    def updated_epoch_millis(self) -> int:
        return pulumi.get(self, "updated_epoch_millis")

    @property
    @pulumi.getter(name="updaterId")
    def updater_id(self) -> str:
        return pulumi.get(self, "updater_id")


class AwaitableGetMetricsPolicyResult(GetMetricsPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMetricsPolicyResult(
            customer=self.customer,
            id=self.id,
            policy_rules=self.policy_rules,
            updated_epoch_millis=self.updated_epoch_millis,
            updater_id=self.updater_id)


def get_metrics_policy(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMetricsPolicyResult:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('wavefront:index/getMetricsPolicy:getMetricsPolicy', __args__, opts=opts, typ=GetMetricsPolicyResult).value

    return AwaitableGetMetricsPolicyResult(
        customer=__ret__.customer,
        id=__ret__.id,
        policy_rules=__ret__.policy_rules,
        updated_epoch_millis=__ret__.updated_epoch_millis,
        updater_id=__ret__.updater_id)
