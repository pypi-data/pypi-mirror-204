# coding=utf-8
# *** WARNING: this file was generated by Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
import pulumi_aws

__all__ = [
    'CDNArgsArgs',
]

@pulumi.input_type
class CDNArgsArgs:
    def __init__(__self__, *,
                 cloudfront_function_associations: Optional[pulumi.Input[Sequence[pulumi.Input['pulumi_aws.cloudfront.DistributionOrderedCacheBehaviorFunctionAssociationArgs']]]] = None,
                 forwarded_values: Optional[pulumi.Input['pulumi_aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesArgs']] = None,
                 lambda_function_associations: Optional[pulumi.Input[Sequence[pulumi.Input['pulumi_aws.cloudfront.DistributionOrderedCacheBehaviorLambdaFunctionAssociationArgs']]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input['pulumi_aws.cloudfront.DistributionOrderedCacheBehaviorFunctionAssociationArgs']]] cloudfront_function_associations: A config block that triggers a cloudfront
               function with specific actions.
        :param pulumi.Input['pulumi_aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesArgs'] forwarded_values: The forwarded values configuration that specifies how CloudFront handles query strings, cookies and headers.
        :param pulumi.Input[Sequence[pulumi.Input['pulumi_aws.cloudfront.DistributionOrderedCacheBehaviorLambdaFunctionAssociationArgs']]] lambda_function_associations: A config block that triggers a lambda
               function with specific actions.
        """
        if cloudfront_function_associations is not None:
            pulumi.set(__self__, "cloudfront_function_associations", cloudfront_function_associations)
        if forwarded_values is not None:
            pulumi.set(__self__, "forwarded_values", forwarded_values)
        if lambda_function_associations is not None:
            pulumi.set(__self__, "lambda_function_associations", lambda_function_associations)

    @property
    @pulumi.getter(name="cloudfrontFunctionAssociations")
    def cloudfront_function_associations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['pulumi_aws.cloudfront.DistributionOrderedCacheBehaviorFunctionAssociationArgs']]]]:
        """
        A config block that triggers a cloudfront
        function with specific actions.
        """
        return pulumi.get(self, "cloudfront_function_associations")

    @cloudfront_function_associations.setter
    def cloudfront_function_associations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['pulumi_aws.cloudfront.DistributionOrderedCacheBehaviorFunctionAssociationArgs']]]]):
        pulumi.set(self, "cloudfront_function_associations", value)

    @property
    @pulumi.getter(name="forwardedValues")
    def forwarded_values(self) -> Optional[pulumi.Input['pulumi_aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesArgs']]:
        """
        The forwarded values configuration that specifies how CloudFront handles query strings, cookies and headers.
        """
        return pulumi.get(self, "forwarded_values")

    @forwarded_values.setter
    def forwarded_values(self, value: Optional[pulumi.Input['pulumi_aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesArgs']]):
        pulumi.set(self, "forwarded_values", value)

    @property
    @pulumi.getter(name="lambdaFunctionAssociations")
    def lambda_function_associations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['pulumi_aws.cloudfront.DistributionOrderedCacheBehaviorLambdaFunctionAssociationArgs']]]]:
        """
        A config block that triggers a lambda
        function with specific actions.
        """
        return pulumi.get(self, "lambda_function_associations")

    @lambda_function_associations.setter
    def lambda_function_associations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['pulumi_aws.cloudfront.DistributionOrderedCacheBehaviorLambdaFunctionAssociationArgs']]]]):
        pulumi.set(self, "lambda_function_associations", value)


