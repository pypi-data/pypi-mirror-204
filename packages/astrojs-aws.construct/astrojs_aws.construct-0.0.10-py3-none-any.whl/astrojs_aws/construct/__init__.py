'''
# Astro Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Introduction

[Astro](https://astro.build/) is the all-in-one web framework designed for speed. This library is supported modes, `static`, `lambda` and `edge`, to deploy astro website to AWS. You can further know it in [https://helbing.github.io/astrojs-aws/](https://helbing.github.io/astrojs-aws/).

## Usage

```python
new astrojsaws.StaticAstroSite(this, "StaticAstroSite", {
  siteDir: "/path/to/dist",
})

new astrojsaws.LambdaAstroSite(this, "LambdaAstroSite", {
  serverEntry: "/path/to/dist/server/entry.mjs",
  staticDir: "/path/to/dist/client",
})

new astrojsaws.EdgeAstroSite(this, "EdgeAstroSite", {
  serverEntry: "/path/to/dist/server/entry.mjs",
  staticDir: "/path/to/dist/client",
})
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_apigatewayv2_alpha as _aws_cdk_aws_apigatewayv2_alpha_050969fe
import aws_cdk.aws_cloudfront as _aws_cdk_aws_cloudfront_ceddda9d
import aws_cdk.aws_cloudfront_origins as _aws_cdk_aws_cloudfront_origins_ceddda9d
import aws_cdk.aws_codeguruprofiler as _aws_cdk_aws_codeguruprofiler_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_lambda_nodejs as _aws_cdk_aws_lambda_nodejs_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@astrojs-aws/construct.AssetsOptions",
    jsii_struct_bases=[],
    name_mapping={"cors": "cors", "errorhtml": "errorhtml", "indexhtml": "indexhtml"},
)
class AssetsOptions:
    def __init__(
        self,
        *,
        cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        errorhtml: typing.Optional[builtins.str] = None,
        indexhtml: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The options for the Assets.

        :param cors: (experimental) The CORS configuration of this bucket. Default: - No CORS configuration.
        :param errorhtml: (experimental) Error document for the website. Default: - error.html
        :param indexhtml: (experimental) Index document for the website. Default: - index.html

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__218269c8e883bfcfc267f8ab52c4306aeb6f115aea330a4a919c790e8ab69aba)
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument errorhtml", value=errorhtml, expected_type=type_hints["errorhtml"])
            check_type(argname="argument indexhtml", value=indexhtml, expected_type=type_hints["indexhtml"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cors is not None:
            self._values["cors"] = cors
        if errorhtml is not None:
            self._values["errorhtml"] = errorhtml
        if indexhtml is not None:
            self._values["indexhtml"] = indexhtml

    @builtins.property
    def cors(self) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.CorsRule]]:
        '''(experimental) The CORS configuration of this bucket.

        :default: - No CORS configuration.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors.html
        :stability: experimental
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.CorsRule]], result)

    @builtins.property
    def errorhtml(self) -> typing.Optional[builtins.str]:
        '''(experimental) Error document for the website.

        :default: - error.html

        :stability: experimental
        '''
        result = self._values.get("errorhtml")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def indexhtml(self) -> typing.Optional[builtins.str]:
        '''(experimental) Index document for the website.

        :default: - index.html

        :stability: experimental
        '''
        result = self._values.get("indexhtml")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssetsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AstroSiteConstruct(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@astrojs-aws/construct.AstroSiteConstruct",
):
    '''(experimental) The base class for all constructs.

    :stability: experimental
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9d982b9095784bc59520b993f10dfaad2bbd6ee2cb8c80aa143a1c8c6d25a8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="newBucket")
    def new_bucket(
        self,
        scope: _constructs_77d1e7e8.Construct,
        wh_enabled: builtins.bool,
        *,
        cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        errorhtml: typing.Optional[builtins.str] = None,
        indexhtml: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_s3_ceddda9d.Bucket:
        '''(experimental) New bucket.

        :param scope: -
        :param wh_enabled: -
        :param cors: (experimental) The CORS configuration of this bucket. Default: - No CORS configuration.
        :param errorhtml: (experimental) Error document for the website. Default: - error.html
        :param indexhtml: (experimental) Index document for the website. Default: - index.html

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a04f0b61812d848db8d60a2935ebfc24eb9b442dc947ccedced2b672fafbcbb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument wh_enabled", value=wh_enabled, expected_type=type_hints["wh_enabled"])
        props = AssetsOptions(cors=cors, errorhtml=errorhtml, indexhtml=indexhtml)

        return typing.cast(_aws_cdk_aws_s3_ceddda9d.Bucket, jsii.invoke(self, "newBucket", [scope, wh_enabled, props]))

    @jsii.member(jsii_name="newDistribution")
    def new_distribution(
        self,
        scope: _constructs_77d1e7e8.Construct,
        default_behavior: typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]],
        *,
        certificate_arn: builtins.str,
        domain: builtins.str,
        cf_functions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.FunctionAssociation, typing.Dict[builtins.str, typing.Any]]]] = None,
        edge_functions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.EdgeLambda, typing.Dict[builtins.str, typing.Any]]]] = None,
        error_responses: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
        geo_restriction: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction] = None,
        log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        log_file_prefix: typing.Optional[builtins.str] = None,
        log_includes_cookies: typing.Optional[builtins.bool] = None,
        price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_cloudfront_ceddda9d.Distribution:
        '''(experimental) New CloudFront distribution.

        :param scope: -
        :param default_behavior: -
        :param certificate_arn: (experimental) Use a custom certificate for the distribution from AWS Certificate Manager (ACM).
        :param domain: (experimental) Domains of the website.
        :param cf_functions: (experimental) The CloudFront functions to invoke before serving the contents. Default: - no new functions will be invoked
        :param edge_functions: (experimental) The Lambda@Edge functions to invoke before serving the contents. Default: - no Lambda functions will be invoked
        :param error_responses: (experimental) How CloudFront should handle requests that are not successful (e.g., PageNotFound). Default: - No custom error responses.
        :param geo_restriction: (experimental) Controls the countries in which your content is distributed. Default: No geo restriction
        :param log_bucket: (experimental) The Amazon S3 bucket to store the access logs in. Default: - if no specified, logs will be disabled.
        :param log_file_prefix: (experimental) An optional string that you want CloudFront to prefix to the access log filenames for this distribution. Default: - no prefix
        :param log_includes_cookies: (experimental) Specifies whether you want CloudFront to include cookies in access logs. Default: false
        :param price_class: (experimental) The price class for the distribution (this impacts how many locations CloudFront uses for your distribution, and billing). Default: PriceClass.PRICE_CLASS_200
        :param web_acl_id: (experimental) Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution. To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``. To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``. Default: - No AWS Web Application Firewall web access control list (web ACL).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f238d74cf0ed25d643ce0509437ee57c57bcca377664798f5511259228173647)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument default_behavior", value=default_behavior, expected_type=type_hints["default_behavior"])
        props = CfOptions(
            certificate_arn=certificate_arn,
            domain=domain,
            cf_functions=cf_functions,
            edge_functions=edge_functions,
            error_responses=error_responses,
            geo_restriction=geo_restriction,
            log_bucket=log_bucket,
            log_file_prefix=log_file_prefix,
            log_includes_cookies=log_includes_cookies,
            price_class=price_class,
            web_acl_id=web_acl_id,
        )

        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.Distribution, jsii.invoke(self, "newDistribution", [scope, default_behavior, props]))

    @jsii.member(jsii_name="newFunction")
    def new_function(
        self,
        scope: _constructs_77d1e7e8.Construct,
        server_entry: builtins.str,
        *,
        bundling: typing.Optional[typing.Union[_aws_cdk_aws_lambda_nodejs_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        runtime: typing.Optional[builtins.str] = None,
        adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        code_signing_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig] = None,
        current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
        filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
        layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> _aws_cdk_aws_lambda_nodejs_ceddda9d.NodejsFunction:
        '''(experimental) New nodejs function.

        :param scope: -
        :param server_entry: -
        :param bundling: (experimental) Bundling options.
        :param runtime: (experimental) The Nodejs Runtime. Default: nodejs18.x
        :param adot_instrumentation: Specify the configuration of AWS Distro for OpenTelemetry (ADOT) instrumentation. Default: - No ADOT instrumentation
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param allow_public_subnet: Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param architecture: The system architectures compatible with this lambda function. Default: Architecture.X86_64
        :param code_signing_config: Code signing config associated with this function. Default: - Not Sign the Code
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. If SNS topic is desired, specify ``deadLetterTopic`` property instead. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param dead_letter_topic: The SNS topic to use as a DLQ. Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly. Default: - no SNS topic
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param environment_encryption: The AWS KMS key that's used to encrypt your function's environment variables. Default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        :param ephemeral_storage_size: The size of the function’s /tmp directory in MiB. Default: 512 MiB
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param insights_version: Specify the version of CloudWatch Lambda insights to use for monitoring. Default: - No Lambda Insights
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param profiling: Enable profiling. Default: - No profiling.
        :param profiling_group: Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param runtime_management_mode: Sets the runtime management configuration for a function's version. Default: Auto
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. This is required when ``vpcSubnets`` is specified. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. This requires ``vpc`` to be specified in order for interfaces to actually be placed in the subnets. If ``vpc`` is not specify, this will raise an error. Note: Internet access for Lambda Functions requires a NAT Gateway, so picking public subnets is not allowed (unless ``allowPublicSubnet`` is set to ``true``). Default: - the Vpc default strategy if not specified
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ed10c38699730e2bf5e69ee0bd4925e438d4799a5852709f308f2affea6d7f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument server_entry", value=server_entry, expected_type=type_hints["server_entry"])
        props = ServerOptions(
            bundling=bundling,
            runtime=runtime,
            adot_instrumentation=adot_instrumentation,
            allow_all_outbound=allow_all_outbound,
            allow_public_subnet=allow_public_subnet,
            architecture=architecture,
            code_signing_config=code_signing_config,
            current_version_options=current_version_options,
            dead_letter_queue=dead_letter_queue,
            dead_letter_queue_enabled=dead_letter_queue_enabled,
            dead_letter_topic=dead_letter_topic,
            description=description,
            environment=environment,
            environment_encryption=environment_encryption,
            ephemeral_storage_size=ephemeral_storage_size,
            events=events,
            filesystem=filesystem,
            function_name=function_name,
            initial_policy=initial_policy,
            insights_version=insights_version,
            layers=layers,
            log_retention=log_retention,
            log_retention_retry_options=log_retention_retry_options,
            log_retention_role=log_retention_role,
            memory_size=memory_size,
            profiling=profiling,
            profiling_group=profiling_group,
            reserved_concurrent_executions=reserved_concurrent_executions,
            role=role,
            runtime_management_mode=runtime_management_mode,
            security_groups=security_groups,
            timeout=timeout,
            tracing=tracing,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            max_event_age=max_event_age,
            on_failure=on_failure,
            on_success=on_success,
            retry_attempts=retry_attempts,
        )

        return typing.cast(_aws_cdk_aws_lambda_nodejs_ceddda9d.NodejsFunction, jsii.invoke(self, "newFunction", [scope, server_entry, props]))

    @jsii.member(jsii_name="newHttpApiGatewayOrigin")
    def new_http_api_gateway_origin(
        self,
        http_api: _aws_cdk_aws_apigatewayv2_alpha_050969fe.HttpApi,
    ) -> _aws_cdk_aws_cloudfront_origins_ceddda9d.HttpOrigin:
        '''(experimental) New HttpApi Gateway origin.

        :param http_api: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77cdc516090f4c6ca63fa8a45cea391f5d98e7ba8127aae15783c36c52203156)
            check_type(argname="argument http_api", value=http_api, expected_type=type_hints["http_api"])
        return typing.cast(_aws_cdk_aws_cloudfront_origins_ceddda9d.HttpOrigin, jsii.invoke(self, "newHttpApiGatewayOrigin", [http_api]))

    @jsii.member(jsii_name="newHttpApiGw")
    def new_http_api_gw(
        self,
        scope: _constructs_77d1e7e8.Construct,
        fn: _aws_cdk_aws_lambda_nodejs_ceddda9d.NodejsFunction,
        *,
        authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        authorizer: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IHttpRouteAuthorizer] = None,
        cors: typing.Optional[typing.Union[_aws_cdk_aws_apigatewayv2_alpha_050969fe.CorsPreflightOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_apigatewayv2_alpha_050969fe.HttpApi:
        '''(experimental) New HttpApi Gateway.

        :param scope: -
        :param fn: -
        :param authorization_scopes: (experimental) OIDC scopes attached to the gateway. Default: - no default authorization scopes
        :param authorizer: (experimental) Authorizer to applied to the gateway. Default: - No authorizer
        :param cors: (experimental) Specifies a CORS configuration for an API. Default: - CORS disabled.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690bef3148c925fc9838340e65c756fdd951c7071af2e83284e14590b1100214)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        props = GwOptions(
            authorization_scopes=authorization_scopes, authorizer=authorizer, cors=cors
        )

        return typing.cast(_aws_cdk_aws_apigatewayv2_alpha_050969fe.HttpApi, jsii.invoke(self, "newHttpApiGw", [scope, fn, props]))

    @jsii.member(jsii_name="newS3Origin")
    def new_s3_origin(
        self,
        scope: _constructs_77d1e7e8.Construct,
        bucket: _aws_cdk_aws_s3_ceddda9d.Bucket,
    ) -> _aws_cdk_aws_cloudfront_origins_ceddda9d.S3Origin:
        '''(experimental) New S3 origin.

        :param scope: -
        :param bucket: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b421adfa617ab976e8d23db7cc054c672a89b03727bc8aea382f4f4d5f4fef2e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(_aws_cdk_aws_cloudfront_origins_ceddda9d.S3Origin, jsii.invoke(self, "newS3Origin", [scope, bucket]))

    @jsii.member(jsii_name="parseRoutesFromDir")
    def parse_routes_from_dir(
        self,
        dir: builtins.str,
        is_cf: typing.Optional[builtins.bool] = None,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Parse routes from directory.

        if the item is directory will parse to {"/item/*": "/item/*"} or {"/item/{proxy+}": "/item/{proxy}"}
        if the item is file will parse to {"/item": "/item"}

        :param dir: -
        :param is_cf: CloudFront route or not, HttpApi Gateway route by defauly, default false.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf3fb2a8029aa3b0236943223b8d34ab2cc4770d3bfaa828c426b76ea51d6cd)
            check_type(argname="argument dir", value=dir, expected_type=type_hints["dir"])
            check_type(argname="argument is_cf", value=is_cf, expected_type=type_hints["is_cf"])
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.invoke(self, "parseRoutesFromDir", [dir, is_cf]))

    @jsii.member(jsii_name="strToRuntime")
    def str_to_runtime(
        self,
        str: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_lambda_ceddda9d.Runtime:
        '''(experimental) Transform string to Runtime.

        :param str: -

        :default: Runtime.NODEJS_18_X

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce4b161f41068601e658dcd2dbe5f267f30e7aa75918596cd3c3a81973920c1)
            check_type(argname="argument str", value=str, expected_type=type_hints["str"])
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Runtime, jsii.invoke(self, "strToRuntime", [str]))


@jsii.data_type(
    jsii_type="@astrojs-aws/construct.CfOptions",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_arn": "certificateArn",
        "domain": "domain",
        "cf_functions": "cfFunctions",
        "edge_functions": "edgeFunctions",
        "error_responses": "errorResponses",
        "geo_restriction": "geoRestriction",
        "log_bucket": "logBucket",
        "log_file_prefix": "logFilePrefix",
        "log_includes_cookies": "logIncludesCookies",
        "price_class": "priceClass",
        "web_acl_id": "webACLId",
    },
)
class CfOptions:
    def __init__(
        self,
        *,
        certificate_arn: builtins.str,
        domain: builtins.str,
        cf_functions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.FunctionAssociation, typing.Dict[builtins.str, typing.Any]]]] = None,
        edge_functions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.EdgeLambda, typing.Dict[builtins.str, typing.Any]]]] = None,
        error_responses: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
        geo_restriction: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction] = None,
        log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        log_file_prefix: typing.Optional[builtins.str] = None,
        log_includes_cookies: typing.Optional[builtins.bool] = None,
        price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) CloudFront options.

        :param certificate_arn: (experimental) Use a custom certificate for the distribution from AWS Certificate Manager (ACM).
        :param domain: (experimental) Domains of the website.
        :param cf_functions: (experimental) The CloudFront functions to invoke before serving the contents. Default: - no new functions will be invoked
        :param edge_functions: (experimental) The Lambda@Edge functions to invoke before serving the contents. Default: - no Lambda functions will be invoked
        :param error_responses: (experimental) How CloudFront should handle requests that are not successful (e.g., PageNotFound). Default: - No custom error responses.
        :param geo_restriction: (experimental) Controls the countries in which your content is distributed. Default: No geo restriction
        :param log_bucket: (experimental) The Amazon S3 bucket to store the access logs in. Default: - if no specified, logs will be disabled.
        :param log_file_prefix: (experimental) An optional string that you want CloudFront to prefix to the access log filenames for this distribution. Default: - no prefix
        :param log_includes_cookies: (experimental) Specifies whether you want CloudFront to include cookies in access logs. Default: false
        :param price_class: (experimental) The price class for the distribution (this impacts how many locations CloudFront uses for your distribution, and billing). Default: PriceClass.PRICE_CLASS_200
        :param web_acl_id: (experimental) Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution. To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``. To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``. Default: - No AWS Web Application Firewall web access control list (web ACL).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4887586fb6a149983ca65cbfb491710351a5dac85c24968ba20dffded138860f)
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument cf_functions", value=cf_functions, expected_type=type_hints["cf_functions"])
            check_type(argname="argument edge_functions", value=edge_functions, expected_type=type_hints["edge_functions"])
            check_type(argname="argument error_responses", value=error_responses, expected_type=type_hints["error_responses"])
            check_type(argname="argument geo_restriction", value=geo_restriction, expected_type=type_hints["geo_restriction"])
            check_type(argname="argument log_bucket", value=log_bucket, expected_type=type_hints["log_bucket"])
            check_type(argname="argument log_file_prefix", value=log_file_prefix, expected_type=type_hints["log_file_prefix"])
            check_type(argname="argument log_includes_cookies", value=log_includes_cookies, expected_type=type_hints["log_includes_cookies"])
            check_type(argname="argument price_class", value=price_class, expected_type=type_hints["price_class"])
            check_type(argname="argument web_acl_id", value=web_acl_id, expected_type=type_hints["web_acl_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_arn": certificate_arn,
            "domain": domain,
        }
        if cf_functions is not None:
            self._values["cf_functions"] = cf_functions
        if edge_functions is not None:
            self._values["edge_functions"] = edge_functions
        if error_responses is not None:
            self._values["error_responses"] = error_responses
        if geo_restriction is not None:
            self._values["geo_restriction"] = geo_restriction
        if log_bucket is not None:
            self._values["log_bucket"] = log_bucket
        if log_file_prefix is not None:
            self._values["log_file_prefix"] = log_file_prefix
        if log_includes_cookies is not None:
            self._values["log_includes_cookies"] = log_includes_cookies
        if price_class is not None:
            self._values["price_class"] = price_class
        if web_acl_id is not None:
            self._values["web_acl_id"] = web_acl_id

    @builtins.property
    def certificate_arn(self) -> builtins.str:
        '''(experimental) Use a custom certificate for the distribution from AWS Certificate Manager (ACM).

        :see: https://aws.amazon.com/premiumsupport/knowledge-center/custom-ssl-certificate-cloudfront/
        :stability: experimental
        '''
        result = self._values.get("certificate_arn")
        assert result is not None, "Required property 'certificate_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain(self) -> builtins.str:
        '''(experimental) Domains of the website.

        :stability: experimental
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cf_functions(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.FunctionAssociation]]:
        '''(experimental) The CloudFront functions to invoke before serving the contents.

        :default: - no new functions will be invoked

        :stability: experimental
        '''
        result = self._values.get("cf_functions")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.FunctionAssociation]], result)

    @builtins.property
    def edge_functions(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.EdgeLambda]]:
        '''(experimental) The Lambda@Edge functions to invoke before serving the contents.

        :default: - no Lambda functions will be invoked

        :see: https://aws.amazon.com/lambda/edge
        :stability: experimental
        '''
        result = self._values.get("edge_functions")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.EdgeLambda]], result)

    @builtins.property
    def error_responses(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse]]:
        '''(experimental) How CloudFront should handle requests that are not successful (e.g., PageNotFound).

        :default: - No custom error responses.

        :stability: experimental
        '''
        result = self._values.get("error_responses")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse]], result)

    @builtins.property
    def geo_restriction(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction]:
        '''(experimental) Controls the countries in which your content is distributed.

        :default: No geo restriction

        :stability: experimental
        '''
        result = self._values.get("geo_restriction")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction], result)

    @builtins.property
    def log_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''(experimental) The Amazon S3 bucket to store the access logs in.

        :default: - if no specified, logs will be disabled.

        :stability: experimental
        '''
        result = self._values.get("log_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def log_file_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional string that you want CloudFront to prefix to the access log filenames for this distribution.

        :default: - no prefix

        :stability: experimental
        '''
        result = self._values.get("log_file_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_includes_cookies(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether you want CloudFront to include cookies in access logs.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("log_includes_cookies")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def price_class(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass]:
        '''(experimental) The price class for the distribution (this impacts how many locations CloudFront uses for your distribution, and billing).

        :default: PriceClass.PRICE_CLASS_200

        :stability: experimental
        '''
        result = self._values.get("price_class")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass], result)

    @builtins.property
    def web_acl_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution.

        To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example
        ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``.

        To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``.

        :default: - No AWS Web Application Firewall web access control list (web ACL).

        :see: https://docs.aws.amazon.com/cloudfront/latest/APIReference/API_CreateDistribution.html#API_CreateDistribution_RequestParameters.
        :stability: experimental
        '''
        result = self._values.get("web_acl_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgeAstroSite(
    AstroSiteConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@astrojs-aws/construct.EdgeAstroSite",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        server_entry: builtins.str,
        static_dir: builtins.str,
        cf_options: typing.Optional[typing.Union[CfOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        only_lambda: typing.Optional[builtins.bool] = None,
        server_options: typing.Optional[typing.Union["ServerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param server_entry: (experimental) The server entry file, e.g. path.join(__dirname, "../server/entry.mjs").
        :param static_dir: (experimental) The directory of static files, e.g. path.join(__dirname, "../dist/client").
        :param cf_options: (experimental) The options for the CloudFront distribution. CloudFront is required, unless ``onlyLambda`` is true. Default: - undefined
        :param only_lambda: (experimental) Only deploy the lambda function for testing, no S3 Bucket and CloudFront. Edge function only works in CloudFront, but it really deploy too slow. Default: - false
        :param server_options: (experimental) The server options.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fbe348a9195063f1a9453096407ebb858ce229e12226bc0c46d7c853af18df9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EdgeAstroSiteProps(
            server_entry=server_entry,
            static_dir=static_dir,
            cf_options=cf_options,
            only_lambda=only_lambda,
            server_options=server_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @builtins.property
    @jsii.member(jsii_name="distributionId")
    def distribution_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "distributionId"))

    @builtins.property
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domains"))

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "functionName"))


@jsii.data_type(
    jsii_type="@astrojs-aws/construct.EdgeAstroSiteProps",
    jsii_struct_bases=[],
    name_mapping={
        "server_entry": "serverEntry",
        "static_dir": "staticDir",
        "cf_options": "cfOptions",
        "only_lambda": "onlyLambda",
        "server_options": "serverOptions",
    },
)
class EdgeAstroSiteProps:
    def __init__(
        self,
        *,
        server_entry: builtins.str,
        static_dir: builtins.str,
        cf_options: typing.Optional[typing.Union[CfOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        only_lambda: typing.Optional[builtins.bool] = None,
        server_options: typing.Optional[typing.Union["ServerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) The options for the EdgeAstroSite.

        :param server_entry: (experimental) The server entry file, e.g. path.join(__dirname, "../server/entry.mjs").
        :param static_dir: (experimental) The directory of static files, e.g. path.join(__dirname, "../dist/client").
        :param cf_options: (experimental) The options for the CloudFront distribution. CloudFront is required, unless ``onlyLambda`` is true. Default: - undefined
        :param only_lambda: (experimental) Only deploy the lambda function for testing, no S3 Bucket and CloudFront. Edge function only works in CloudFront, but it really deploy too slow. Default: - false
        :param server_options: (experimental) The server options.

        :stability: experimental
        '''
        if isinstance(cf_options, dict):
            cf_options = CfOptions(**cf_options)
        if isinstance(server_options, dict):
            server_options = ServerOptions(**server_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8305299a6901c6df438fea789539465c466d30dc2750bc7f5ce3caa6c5fd264)
            check_type(argname="argument server_entry", value=server_entry, expected_type=type_hints["server_entry"])
            check_type(argname="argument static_dir", value=static_dir, expected_type=type_hints["static_dir"])
            check_type(argname="argument cf_options", value=cf_options, expected_type=type_hints["cf_options"])
            check_type(argname="argument only_lambda", value=only_lambda, expected_type=type_hints["only_lambda"])
            check_type(argname="argument server_options", value=server_options, expected_type=type_hints["server_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "server_entry": server_entry,
            "static_dir": static_dir,
        }
        if cf_options is not None:
            self._values["cf_options"] = cf_options
        if only_lambda is not None:
            self._values["only_lambda"] = only_lambda
        if server_options is not None:
            self._values["server_options"] = server_options

    @builtins.property
    def server_entry(self) -> builtins.str:
        '''(experimental) The server entry file, e.g. path.join(__dirname, "../server/entry.mjs").

        :stability: experimental
        '''
        result = self._values.get("server_entry")
        assert result is not None, "Required property 'server_entry' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def static_dir(self) -> builtins.str:
        '''(experimental) The directory of static files, e.g. path.join(__dirname, "../dist/client").

        :stability: experimental
        '''
        result = self._values.get("static_dir")
        assert result is not None, "Required property 'static_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cf_options(self) -> typing.Optional[CfOptions]:
        '''(experimental) The options for the CloudFront distribution.

        CloudFront is required, unless ``onlyLambda`` is true.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("cf_options")
        return typing.cast(typing.Optional[CfOptions], result)

    @builtins.property
    def only_lambda(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Only deploy the lambda function for testing, no S3 Bucket and CloudFront.

        Edge function only works in CloudFront, but it really deploy too slow.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("only_lambda")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def server_options(self) -> typing.Optional["ServerOptions"]:
        '''(experimental) The server options.

        :stability: experimental
        '''
        result = self._values.get("server_options")
        return typing.cast(typing.Optional["ServerOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgeAstroSiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@astrojs-aws/construct.GwOptions",
    jsii_struct_bases=[],
    name_mapping={
        "authorization_scopes": "authorizationScopes",
        "authorizer": "authorizer",
        "cors": "cors",
    },
)
class GwOptions:
    def __init__(
        self,
        *,
        authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        authorizer: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IHttpRouteAuthorizer] = None,
        cors: typing.Optional[typing.Union[_aws_cdk_aws_apigatewayv2_alpha_050969fe.CorsPreflightOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) The options for the CloudFront distribution.

        :param authorization_scopes: (experimental) OIDC scopes attached to the gateway. Default: - no default authorization scopes
        :param authorizer: (experimental) Authorizer to applied to the gateway. Default: - No authorizer
        :param cors: (experimental) Specifies a CORS configuration for an API. Default: - CORS disabled.

        :stability: experimental
        '''
        if isinstance(cors, dict):
            cors = _aws_cdk_aws_apigatewayv2_alpha_050969fe.CorsPreflightOptions(**cors)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073e959e71ff8a469fc46ec57cb97ee27ebc49323b8cc6611a53d874ee5266dd)
            check_type(argname="argument authorization_scopes", value=authorization_scopes, expected_type=type_hints["authorization_scopes"])
            check_type(argname="argument authorizer", value=authorizer, expected_type=type_hints["authorizer"])
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorization_scopes is not None:
            self._values["authorization_scopes"] = authorization_scopes
        if authorizer is not None:
            self._values["authorizer"] = authorizer
        if cors is not None:
            self._values["cors"] = cors

    @builtins.property
    def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) OIDC scopes attached to the gateway.

        :default: - no default authorization scopes

        :stability: experimental
        '''
        result = self._values.get("authorization_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def authorizer(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IHttpRouteAuthorizer]:
        '''(experimental) Authorizer to applied to the gateway.

        :default: - No authorizer

        :stability: experimental
        '''
        result = self._values.get("authorizer")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IHttpRouteAuthorizer], result)

    @builtins.property
    def cors(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.CorsPreflightOptions]:
        '''(experimental) Specifies a CORS configuration for an API.

        :default: - CORS disabled.

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html
        :stability: experimental
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.CorsPreflightOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GwOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaAstroSite(
    AstroSiteConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@astrojs-aws/construct.LambdaAstroSite",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        server_entry: builtins.str,
        static_dir: builtins.str,
        cf_options: typing.Optional[typing.Union[CfOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gw_options: typing.Optional[typing.Union[GwOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        server_options: typing.Optional[typing.Union["ServerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param server_entry: (experimental) The server entry file, e.g. path.join(__dirname, "../server/entry.mjs").
        :param static_dir: (experimental) The directory of static files, e.g. path.join(__dirname, "../dist/client").
        :param cf_options: (experimental) The options for the CloudFront distribution. Recommended to use CloudFront for production. Default: - No CloudFront distribution, if not equal to undefined, CloudFront auto-enabled.
        :param gw_options: (experimental) HttpApi Gateway options.
        :param server_options: (experimental) The server options.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__919d2f7c50a313b0018ea18c98ec6f7aab019e1ede4395a72ac4ffe9cdb385b5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaAstroSiteProps(
            server_entry=server_entry,
            static_dir=static_dir,
            cf_options=cf_options,
            gw_options=gw_options,
            server_options=server_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @builtins.property
    @jsii.member(jsii_name="distributionId")
    def distribution_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "distributionId"))

    @builtins.property
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domains"))

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "functionName"))


@jsii.data_type(
    jsii_type="@astrojs-aws/construct.LambdaAstroSiteProps",
    jsii_struct_bases=[],
    name_mapping={
        "server_entry": "serverEntry",
        "static_dir": "staticDir",
        "cf_options": "cfOptions",
        "gw_options": "gwOptions",
        "server_options": "serverOptions",
    },
)
class LambdaAstroSiteProps:
    def __init__(
        self,
        *,
        server_entry: builtins.str,
        static_dir: builtins.str,
        cf_options: typing.Optional[typing.Union[CfOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gw_options: typing.Optional[typing.Union[GwOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        server_options: typing.Optional[typing.Union["ServerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) The options for the LambdaAstroSite.

        :param server_entry: (experimental) The server entry file, e.g. path.join(__dirname, "../server/entry.mjs").
        :param static_dir: (experimental) The directory of static files, e.g. path.join(__dirname, "../dist/client").
        :param cf_options: (experimental) The options for the CloudFront distribution. Recommended to use CloudFront for production. Default: - No CloudFront distribution, if not equal to undefined, CloudFront auto-enabled.
        :param gw_options: (experimental) HttpApi Gateway options.
        :param server_options: (experimental) The server options.

        :stability: experimental
        '''
        if isinstance(cf_options, dict):
            cf_options = CfOptions(**cf_options)
        if isinstance(gw_options, dict):
            gw_options = GwOptions(**gw_options)
        if isinstance(server_options, dict):
            server_options = ServerOptions(**server_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3efb3975e83a8896ea9851eccf4181ddb1252978a00a5d4e0125d4525ea8fd4)
            check_type(argname="argument server_entry", value=server_entry, expected_type=type_hints["server_entry"])
            check_type(argname="argument static_dir", value=static_dir, expected_type=type_hints["static_dir"])
            check_type(argname="argument cf_options", value=cf_options, expected_type=type_hints["cf_options"])
            check_type(argname="argument gw_options", value=gw_options, expected_type=type_hints["gw_options"])
            check_type(argname="argument server_options", value=server_options, expected_type=type_hints["server_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "server_entry": server_entry,
            "static_dir": static_dir,
        }
        if cf_options is not None:
            self._values["cf_options"] = cf_options
        if gw_options is not None:
            self._values["gw_options"] = gw_options
        if server_options is not None:
            self._values["server_options"] = server_options

    @builtins.property
    def server_entry(self) -> builtins.str:
        '''(experimental) The server entry file, e.g. path.join(__dirname, "../server/entry.mjs").

        :stability: experimental
        '''
        result = self._values.get("server_entry")
        assert result is not None, "Required property 'server_entry' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def static_dir(self) -> builtins.str:
        '''(experimental) The directory of static files, e.g. path.join(__dirname, "../dist/client").

        :stability: experimental
        '''
        result = self._values.get("static_dir")
        assert result is not None, "Required property 'static_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cf_options(self) -> typing.Optional[CfOptions]:
        '''(experimental) The options for the CloudFront distribution.

        Recommended to use CloudFront for production.

        :default: - No CloudFront distribution, if not equal to undefined, CloudFront auto-enabled.

        :stability: experimental
        '''
        result = self._values.get("cf_options")
        return typing.cast(typing.Optional[CfOptions], result)

    @builtins.property
    def gw_options(self) -> typing.Optional[GwOptions]:
        '''(experimental) HttpApi Gateway options.

        :stability: experimental
        '''
        result = self._values.get("gw_options")
        return typing.cast(typing.Optional[GwOptions], result)

    @builtins.property
    def server_options(self) -> typing.Optional["ServerOptions"]:
        '''(experimental) The server options.

        :stability: experimental
        '''
        result = self._values.get("server_options")
        return typing.cast(typing.Optional["ServerOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaAstroSiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@astrojs-aws/construct.ServerOptions",
    jsii_struct_bases=[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions],
    name_mapping={
        "max_event_age": "maxEventAge",
        "on_failure": "onFailure",
        "on_success": "onSuccess",
        "retry_attempts": "retryAttempts",
        "adot_instrumentation": "adotInstrumentation",
        "allow_all_outbound": "allowAllOutbound",
        "allow_public_subnet": "allowPublicSubnet",
        "architecture": "architecture",
        "code_signing_config": "codeSigningConfig",
        "current_version_options": "currentVersionOptions",
        "dead_letter_queue": "deadLetterQueue",
        "dead_letter_queue_enabled": "deadLetterQueueEnabled",
        "dead_letter_topic": "deadLetterTopic",
        "description": "description",
        "environment": "environment",
        "environment_encryption": "environmentEncryption",
        "ephemeral_storage_size": "ephemeralStorageSize",
        "events": "events",
        "filesystem": "filesystem",
        "function_name": "functionName",
        "initial_policy": "initialPolicy",
        "insights_version": "insightsVersion",
        "layers": "layers",
        "log_retention": "logRetention",
        "log_retention_retry_options": "logRetentionRetryOptions",
        "log_retention_role": "logRetentionRole",
        "memory_size": "memorySize",
        "profiling": "profiling",
        "profiling_group": "profilingGroup",
        "reserved_concurrent_executions": "reservedConcurrentExecutions",
        "role": "role",
        "runtime_management_mode": "runtimeManagementMode",
        "security_groups": "securityGroups",
        "timeout": "timeout",
        "tracing": "tracing",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "bundling": "bundling",
        "runtime": "runtime",
    },
)
class ServerOptions(_aws_cdk_aws_lambda_ceddda9d.FunctionOptions):
    def __init__(
        self,
        *,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        code_signing_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig] = None,
        current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
        filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
        layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        bundling: typing.Optional[typing.Union[_aws_cdk_aws_lambda_nodejs_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        runtime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The options for the lambda function.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param adot_instrumentation: Specify the configuration of AWS Distro for OpenTelemetry (ADOT) instrumentation. Default: - No ADOT instrumentation
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param allow_public_subnet: Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param architecture: The system architectures compatible with this lambda function. Default: Architecture.X86_64
        :param code_signing_config: Code signing config associated with this function. Default: - Not Sign the Code
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. If SNS topic is desired, specify ``deadLetterTopic`` property instead. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param dead_letter_topic: The SNS topic to use as a DLQ. Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly. Default: - no SNS topic
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param environment_encryption: The AWS KMS key that's used to encrypt your function's environment variables. Default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        :param ephemeral_storage_size: The size of the function’s /tmp directory in MiB. Default: 512 MiB
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param insights_version: Specify the version of CloudWatch Lambda insights to use for monitoring. Default: - No Lambda Insights
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param profiling: Enable profiling. Default: - No profiling.
        :param profiling_group: Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param runtime_management_mode: Sets the runtime management configuration for a function's version. Default: Auto
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. This is required when ``vpcSubnets`` is specified. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. This requires ``vpc`` to be specified in order for interfaces to actually be placed in the subnets. If ``vpc`` is not specify, this will raise an error. Note: Internet access for Lambda Functions requires a NAT Gateway, so picking public subnets is not allowed (unless ``allowPublicSubnet`` is set to ``true``). Default: - the Vpc default strategy if not specified
        :param bundling: (experimental) Bundling options.
        :param runtime: (experimental) The Nodejs Runtime. Default: nodejs18.x

        :stability: experimental
        '''
        if isinstance(adot_instrumentation, dict):
            adot_instrumentation = _aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig(**adot_instrumentation)
        if isinstance(current_version_options, dict):
            current_version_options = _aws_cdk_aws_lambda_ceddda9d.VersionOptions(**current_version_options)
        if isinstance(log_retention_retry_options, dict):
            log_retention_retry_options = _aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions(**log_retention_retry_options)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if isinstance(bundling, dict):
            bundling = _aws_cdk_aws_lambda_nodejs_ceddda9d.BundlingOptions(**bundling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37953f1eba9b563d1341cf75bd7d73a57ac96383b9d4bbcb3ad5ab140341b32e)
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            check_type(argname="argument on_success", value=on_success, expected_type=type_hints["on_success"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument adot_instrumentation", value=adot_instrumentation, expected_type=type_hints["adot_instrumentation"])
            check_type(argname="argument allow_all_outbound", value=allow_all_outbound, expected_type=type_hints["allow_all_outbound"])
            check_type(argname="argument allow_public_subnet", value=allow_public_subnet, expected_type=type_hints["allow_public_subnet"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument code_signing_config", value=code_signing_config, expected_type=type_hints["code_signing_config"])
            check_type(argname="argument current_version_options", value=current_version_options, expected_type=type_hints["current_version_options"])
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument dead_letter_queue_enabled", value=dead_letter_queue_enabled, expected_type=type_hints["dead_letter_queue_enabled"])
            check_type(argname="argument dead_letter_topic", value=dead_letter_topic, expected_type=type_hints["dead_letter_topic"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument environment_encryption", value=environment_encryption, expected_type=type_hints["environment_encryption"])
            check_type(argname="argument ephemeral_storage_size", value=ephemeral_storage_size, expected_type=type_hints["ephemeral_storage_size"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument filesystem", value=filesystem, expected_type=type_hints["filesystem"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument initial_policy", value=initial_policy, expected_type=type_hints["initial_policy"])
            check_type(argname="argument insights_version", value=insights_version, expected_type=type_hints["insights_version"])
            check_type(argname="argument layers", value=layers, expected_type=type_hints["layers"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument log_retention_retry_options", value=log_retention_retry_options, expected_type=type_hints["log_retention_retry_options"])
            check_type(argname="argument log_retention_role", value=log_retention_role, expected_type=type_hints["log_retention_role"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument profiling", value=profiling, expected_type=type_hints["profiling"])
            check_type(argname="argument profiling_group", value=profiling_group, expected_type=type_hints["profiling_group"])
            check_type(argname="argument reserved_concurrent_executions", value=reserved_concurrent_executions, expected_type=type_hints["reserved_concurrent_executions"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument runtime_management_mode", value=runtime_management_mode, expected_type=type_hints["runtime_management_mode"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument tracing", value=tracing, expected_type=type_hints["tracing"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument bundling", value=bundling, expected_type=type_hints["bundling"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if on_success is not None:
            self._values["on_success"] = on_success
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if adot_instrumentation is not None:
            self._values["adot_instrumentation"] = adot_instrumentation
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if allow_public_subnet is not None:
            self._values["allow_public_subnet"] = allow_public_subnet
        if architecture is not None:
            self._values["architecture"] = architecture
        if code_signing_config is not None:
            self._values["code_signing_config"] = code_signing_config
        if current_version_options is not None:
            self._values["current_version_options"] = current_version_options
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if dead_letter_queue_enabled is not None:
            self._values["dead_letter_queue_enabled"] = dead_letter_queue_enabled
        if dead_letter_topic is not None:
            self._values["dead_letter_topic"] = dead_letter_topic
        if description is not None:
            self._values["description"] = description
        if environment is not None:
            self._values["environment"] = environment
        if environment_encryption is not None:
            self._values["environment_encryption"] = environment_encryption
        if ephemeral_storage_size is not None:
            self._values["ephemeral_storage_size"] = ephemeral_storage_size
        if events is not None:
            self._values["events"] = events
        if filesystem is not None:
            self._values["filesystem"] = filesystem
        if function_name is not None:
            self._values["function_name"] = function_name
        if initial_policy is not None:
            self._values["initial_policy"] = initial_policy
        if insights_version is not None:
            self._values["insights_version"] = insights_version
        if layers is not None:
            self._values["layers"] = layers
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if log_retention_retry_options is not None:
            self._values["log_retention_retry_options"] = log_retention_retry_options
        if log_retention_role is not None:
            self._values["log_retention_role"] = log_retention_role
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if profiling is not None:
            self._values["profiling"] = profiling
        if profiling_group is not None:
            self._values["profiling_group"] = profiling_group
        if reserved_concurrent_executions is not None:
            self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None:
            self._values["role"] = role
        if runtime_management_mode is not None:
            self._values["runtime_management_mode"] = runtime_management_mode
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if timeout is not None:
            self._values["timeout"] = timeout
        if tracing is not None:
            self._values["tracing"] = tracing
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if bundling is not None:
            self._values["bundling"] = bundling
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        :default: Duration.hours(6)
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def on_failure(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination]:
        '''The destination for failed invocations.

        :default: - no destination
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination], result)

    @builtins.property
    def on_success(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination]:
        '''The destination for successful invocations.

        :default: - no destination
        '''
        result = self._values.get("on_success")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        :default: 2
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def adot_instrumentation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig]:
        '''Specify the configuration of AWS Distro for OpenTelemetry (ADOT) instrumentation.

        :default: - No ADOT instrumentation

        :see: https://aws-otel.github.io/docs/getting-started/lambda
        '''
        result = self._values.get("adot_instrumentation")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig], result)

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        '''Whether to allow the Lambda to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        Lambda to connect to network targets.

        :default: true
        '''
        result = self._values.get("allow_all_outbound")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_public_subnet(self) -> typing.Optional[builtins.bool]:
        '''Lambda Functions in a public subnet can NOT access the internet.

        Use this property to acknowledge this limitation and still place the function in a public subnet.

        :default: false

        :see: https://stackoverflow.com/questions/52992085/why-cant-an-aws-lambda-function-inside-a-public-subnet-in-a-vpc-connect-to-the/52994841#52994841
        '''
        result = self._values.get("allow_public_subnet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def architecture(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture]:
        '''The system architectures compatible with this lambda function.

        :default: Architecture.X86_64
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture], result)

    @builtins.property
    def code_signing_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig]:
        '''Code signing config associated with this function.

        :default: - Not Sign the Code
        '''
        result = self._values.get("code_signing_config")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig], result)

    @builtins.property
    def current_version_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.VersionOptions]:
        '''Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method.

        :default: - default options as described in ``VersionOptions``
        '''
        result = self._values.get("current_version_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.VersionOptions], result)

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''The SQS queue to use if DLQ is enabled.

        If SNS topic is desired, specify ``deadLetterTopic`` property instead.

        :default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def dead_letter_queue_enabled(self) -> typing.Optional[builtins.bool]:
        '''Enabled DLQ.

        If ``deadLetterQueue`` is undefined,
        an SQS queue with default options will be defined for your Function.

        :default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        '''
        result = self._values.get("dead_letter_queue_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dead_letter_topic(self) -> typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic]:
        '''The SNS topic to use as a DLQ.

        Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created
        rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly.

        :default: - no SNS topic
        '''
        result = self._values.get("dead_letter_topic")
        return typing.cast(typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the function.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key-value pairs that Lambda caches and makes available for your Lambda functions.

        Use environment variables to apply configuration changes, such
        as test and production environment configurations, without changing your
        Lambda function source code.

        :default: - No environment variables.
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment_encryption(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The AWS KMS key that's used to encrypt your function's environment variables.

        :default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        '''
        result = self._values.get("environment_encryption")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def ephemeral_storage_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''The size of the function’s /tmp directory in MiB.

        :default: 512 MiB
        '''
        result = self._values.get("ephemeral_storage_size")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def events(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.IEventSource]]:
        '''Event sources for this function.

        You can also add event sources using ``addEventSource``.

        :default: - No event sources.
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.IEventSource]], result)

    @builtins.property
    def filesystem(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem]:
        '''The filesystem configuration for the lambda function.

        :default: - will not mount any filesystem
        '''
        result = self._values.get("filesystem")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''A name for the function.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
        ID for the function's name. For more information, see Name Type.
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_policy(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]]:
        '''Initial policy statements to add to the created Lambda Role.

        You can call ``addToRolePolicy`` to the created lambda to add statements post creation.

        :default: - No policy statements are added to the created Lambda role.
        '''
        result = self._values.get("initial_policy")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]], result)

    @builtins.property
    def insights_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion]:
        '''Specify the version of CloudWatch Lambda insights to use for monitoring.

        :default: - No Lambda Insights

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights-Getting-Started-docker.html
        '''
        result = self._values.get("insights_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion], result)

    @builtins.property
    def layers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]]:
        '''A list of layers to add to the function's execution environment.

        You can configure your Lambda function to pull in
        additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies
        that can be used by multiple functions.

        :default: - No layers.
        '''
        result = self._values.get("layers")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.INFINITE
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def log_retention_retry_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions]:
        '''When log retention is specified, a custom resource attempts to create the CloudWatch log group.

        These options control the retry policy when interacting with CloudWatch APIs.

        :default: - Default AWS SDK retry options.
        '''
        result = self._values.get("log_retention_retry_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions], result)

    @builtins.property
    def log_retention_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        :default: - A new role is created.
        '''
        result = self._values.get("log_retention_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''The amount of memory, in MB, that is allocated to your Lambda function.

        Lambda uses this value to proportionally allocate the amount of CPU
        power. For more information, see Resource Model in the AWS Lambda
        Developer Guide.

        :default: 128
        '''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def profiling(self) -> typing.Optional[builtins.bool]:
        '''Enable profiling.

        :default: - No profiling.

        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        '''
        result = self._values.get("profiling")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def profiling_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup]:
        '''Profiling Group.

        :default: - A new profiling group will be created if ``profiling`` is set.

        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        '''
        result = self._values.get("profiling_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup], result)

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        '''The maximum of concurrent executions you want to reserve for the function.

        :default: - No specific limit - account limit.

        :see: https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html
        '''
        result = self._values.get("reserved_concurrent_executions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''Lambda execution role.

        This is the role that will be assumed by the function upon execution.
        It controls the permissions that the function will have. The Role must
        be assumable by the 'lambda.amazonaws.com' service principal.

        The default Role automatically has permissions granted for Lambda execution. If you
        provide a Role, you must add the relevant AWS managed policies yourself.

        The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and
        "service-role/AWSLambdaVPCAccessExecutionRole".

        :default:

        - A unique role will be generated for this lambda function.
        Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def runtime_management_mode(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode]:
        '''Sets the runtime management configuration for a function's version.

        :default: Auto
        '''
        result = self._values.get("runtime_management_mode")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''The list of security groups to associate with the Lambda's network interfaces.

        Only used if 'vpc' is supplied.

        :default:

        - If the function is placed within a VPC and a security group is
        not specified, either by this or securityGroup prop, a dedicated security
        group will be created for this function.
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The function execution time (in seconds) after which Lambda terminates the function.

        Because the execution time affects cost, set this value
        based on the function's expected execution time.

        :default: Duration.seconds(3)
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def tracing(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing]:
        '''Enable AWS X-Ray Tracing for Lambda Function.

        :default: Tracing.Disabled
        '''
        result = self._values.get("tracing")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''VPC network to place Lambda network interfaces.

        Specify this if the Lambda function needs to access resources in a VPC.
        This is required when ``vpcSubnets`` is specified.

        :default: - Function is not placed within a VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Where to place the network interfaces within the VPC.

        This requires ``vpc`` to be specified in order for interfaces to actually be
        placed in the subnets. If ``vpc`` is not specify, this will raise an error.

        Note: Internet access for Lambda Functions requires a NAT Gateway, so picking
        public subnets is not allowed (unless ``allowPublicSubnet`` is set to ``true``).

        :default: - the Vpc default strategy if not specified
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def bundling(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_nodejs_ceddda9d.BundlingOptions]:
        '''(experimental) Bundling options.

        :stability: experimental
        '''
        result = self._values.get("bundling")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_nodejs_ceddda9d.BundlingOptions], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Nodejs Runtime.

        :default: nodejs18.x

        :stability: experimental
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StaticAstroSite(
    AstroSiteConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@astrojs-aws/construct.StaticAstroSite",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        site_dir: builtins.str,
        cf_options: typing.Optional[typing.Union[CfOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        errorhtml: typing.Optional[builtins.str] = None,
        indexhtml: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param site_dir: (experimental) The directory of built files, e.g. path.join(__dirname, "../dist").
        :param cf_options: (experimental) The options for the CloudFront distribution. Default: - No CloudFront distribution, if not equal to undefined, CloudFront auto-enabled.
        :param cors: (experimental) The CORS configuration of this bucket. Default: - No CORS configuration.
        :param errorhtml: (experimental) Error document for the website. Default: - error.html
        :param indexhtml: (experimental) Index document for the website. Default: - index.html

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7c1078f47a089ec32759a5895dbdd9baee0042d6d1f2f5014d04a76b084ca0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StaticAstroSiteProps(
            site_dir=site_dir,
            cf_options=cf_options,
            cors=cors,
            errorhtml=errorhtml,
            indexhtml=indexhtml,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @builtins.property
    @jsii.member(jsii_name="distributionId")
    def distribution_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "distributionId"))

    @builtins.property
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domains"))


@jsii.data_type(
    jsii_type="@astrojs-aws/construct.StaticAstroSiteProps",
    jsii_struct_bases=[AssetsOptions],
    name_mapping={
        "cors": "cors",
        "errorhtml": "errorhtml",
        "indexhtml": "indexhtml",
        "site_dir": "siteDir",
        "cf_options": "cfOptions",
    },
)
class StaticAstroSiteProps(AssetsOptions):
    def __init__(
        self,
        *,
        cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        errorhtml: typing.Optional[builtins.str] = None,
        indexhtml: typing.Optional[builtins.str] = None,
        site_dir: builtins.str,
        cf_options: typing.Optional[typing.Union[CfOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) The options for the StaticAstroSite.

        :param cors: (experimental) The CORS configuration of this bucket. Default: - No CORS configuration.
        :param errorhtml: (experimental) Error document for the website. Default: - error.html
        :param indexhtml: (experimental) Index document for the website. Default: - index.html
        :param site_dir: (experimental) The directory of built files, e.g. path.join(__dirname, "../dist").
        :param cf_options: (experimental) The options for the CloudFront distribution. Default: - No CloudFront distribution, if not equal to undefined, CloudFront auto-enabled.

        :stability: experimental
        '''
        if isinstance(cf_options, dict):
            cf_options = CfOptions(**cf_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3325321ebadc5e36cd8f3b8ad8b45edb7386a70e17bc2b7a0976fb7ae04ab39e)
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument errorhtml", value=errorhtml, expected_type=type_hints["errorhtml"])
            check_type(argname="argument indexhtml", value=indexhtml, expected_type=type_hints["indexhtml"])
            check_type(argname="argument site_dir", value=site_dir, expected_type=type_hints["site_dir"])
            check_type(argname="argument cf_options", value=cf_options, expected_type=type_hints["cf_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "site_dir": site_dir,
        }
        if cors is not None:
            self._values["cors"] = cors
        if errorhtml is not None:
            self._values["errorhtml"] = errorhtml
        if indexhtml is not None:
            self._values["indexhtml"] = indexhtml
        if cf_options is not None:
            self._values["cf_options"] = cf_options

    @builtins.property
    def cors(self) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.CorsRule]]:
        '''(experimental) The CORS configuration of this bucket.

        :default: - No CORS configuration.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors.html
        :stability: experimental
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.CorsRule]], result)

    @builtins.property
    def errorhtml(self) -> typing.Optional[builtins.str]:
        '''(experimental) Error document for the website.

        :default: - error.html

        :stability: experimental
        '''
        result = self._values.get("errorhtml")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def indexhtml(self) -> typing.Optional[builtins.str]:
        '''(experimental) Index document for the website.

        :default: - index.html

        :stability: experimental
        '''
        result = self._values.get("indexhtml")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def site_dir(self) -> builtins.str:
        '''(experimental) The directory of built files, e.g. path.join(__dirname, "../dist").

        :stability: experimental
        '''
        result = self._values.get("site_dir")
        assert result is not None, "Required property 'site_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cf_options(self) -> typing.Optional[CfOptions]:
        '''(experimental) The options for the CloudFront distribution.

        :default: - No CloudFront distribution, if not equal to undefined, CloudFront auto-enabled.

        :stability: experimental
        '''
        result = self._values.get("cf_options")
        return typing.cast(typing.Optional[CfOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StaticAstroSiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AssetsOptions",
    "AstroSiteConstruct",
    "CfOptions",
    "EdgeAstroSite",
    "EdgeAstroSiteProps",
    "GwOptions",
    "LambdaAstroSite",
    "LambdaAstroSiteProps",
    "ServerOptions",
    "StaticAstroSite",
    "StaticAstroSiteProps",
]

publication.publish()

def _typecheckingstub__218269c8e883bfcfc267f8ab52c4306aeb6f115aea330a4a919c790e8ab69aba(
    *,
    cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    errorhtml: typing.Optional[builtins.str] = None,
    indexhtml: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9d982b9095784bc59520b993f10dfaad2bbd6ee2cb8c80aa143a1c8c6d25a8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a04f0b61812d848db8d60a2935ebfc24eb9b442dc947ccedced2b672fafbcbb(
    scope: _constructs_77d1e7e8.Construct,
    wh_enabled: builtins.bool,
    *,
    cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    errorhtml: typing.Optional[builtins.str] = None,
    indexhtml: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f238d74cf0ed25d643ce0509437ee57c57bcca377664798f5511259228173647(
    scope: _constructs_77d1e7e8.Construct,
    default_behavior: typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]],
    *,
    certificate_arn: builtins.str,
    domain: builtins.str,
    cf_functions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.FunctionAssociation, typing.Dict[builtins.str, typing.Any]]]] = None,
    edge_functions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.EdgeLambda, typing.Dict[builtins.str, typing.Any]]]] = None,
    error_responses: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
    geo_restriction: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction] = None,
    log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    log_file_prefix: typing.Optional[builtins.str] = None,
    log_includes_cookies: typing.Optional[builtins.bool] = None,
    price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
    web_acl_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ed10c38699730e2bf5e69ee0bd4925e438d4799a5852709f308f2affea6d7f(
    scope: _constructs_77d1e7e8.Construct,
    server_entry: builtins.str,
    *,
    bundling: typing.Optional[typing.Union[_aws_cdk_aws_lambda_nodejs_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime: typing.Optional[builtins.str] = None,
    adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    allow_public_subnet: typing.Optional[builtins.bool] = None,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    code_signing_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig] = None,
    current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
    dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment_encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
    filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
    function_name: typing.Optional[builtins.str] = None,
    initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
    layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    profiling: typing.Optional[builtins.bool] = None,
    profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77cdc516090f4c6ca63fa8a45cea391f5d98e7ba8127aae15783c36c52203156(
    http_api: _aws_cdk_aws_apigatewayv2_alpha_050969fe.HttpApi,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690bef3148c925fc9838340e65c756fdd951c7071af2e83284e14590b1100214(
    scope: _constructs_77d1e7e8.Construct,
    fn: _aws_cdk_aws_lambda_nodejs_ceddda9d.NodejsFunction,
    *,
    authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    authorizer: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IHttpRouteAuthorizer] = None,
    cors: typing.Optional[typing.Union[_aws_cdk_aws_apigatewayv2_alpha_050969fe.CorsPreflightOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b421adfa617ab976e8d23db7cc054c672a89b03727bc8aea382f4f4d5f4fef2e(
    scope: _constructs_77d1e7e8.Construct,
    bucket: _aws_cdk_aws_s3_ceddda9d.Bucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf3fb2a8029aa3b0236943223b8d34ab2cc4770d3bfaa828c426b76ea51d6cd(
    dir: builtins.str,
    is_cf: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce4b161f41068601e658dcd2dbe5f267f30e7aa75918596cd3c3a81973920c1(
    str: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4887586fb6a149983ca65cbfb491710351a5dac85c24968ba20dffded138860f(
    *,
    certificate_arn: builtins.str,
    domain: builtins.str,
    cf_functions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.FunctionAssociation, typing.Dict[builtins.str, typing.Any]]]] = None,
    edge_functions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.EdgeLambda, typing.Dict[builtins.str, typing.Any]]]] = None,
    error_responses: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
    geo_restriction: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction] = None,
    log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    log_file_prefix: typing.Optional[builtins.str] = None,
    log_includes_cookies: typing.Optional[builtins.bool] = None,
    price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
    web_acl_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fbe348a9195063f1a9453096407ebb858ce229e12226bc0c46d7c853af18df9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    server_entry: builtins.str,
    static_dir: builtins.str,
    cf_options: typing.Optional[typing.Union[CfOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    only_lambda: typing.Optional[builtins.bool] = None,
    server_options: typing.Optional[typing.Union[ServerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8305299a6901c6df438fea789539465c466d30dc2750bc7f5ce3caa6c5fd264(
    *,
    server_entry: builtins.str,
    static_dir: builtins.str,
    cf_options: typing.Optional[typing.Union[CfOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    only_lambda: typing.Optional[builtins.bool] = None,
    server_options: typing.Optional[typing.Union[ServerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073e959e71ff8a469fc46ec57cb97ee27ebc49323b8cc6611a53d874ee5266dd(
    *,
    authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    authorizer: typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.IHttpRouteAuthorizer] = None,
    cors: typing.Optional[typing.Union[_aws_cdk_aws_apigatewayv2_alpha_050969fe.CorsPreflightOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919d2f7c50a313b0018ea18c98ec6f7aab019e1ede4395a72ac4ffe9cdb385b5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    server_entry: builtins.str,
    static_dir: builtins.str,
    cf_options: typing.Optional[typing.Union[CfOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gw_options: typing.Optional[typing.Union[GwOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    server_options: typing.Optional[typing.Union[ServerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3efb3975e83a8896ea9851eccf4181ddb1252978a00a5d4e0125d4525ea8fd4(
    *,
    server_entry: builtins.str,
    static_dir: builtins.str,
    cf_options: typing.Optional[typing.Union[CfOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gw_options: typing.Optional[typing.Union[GwOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    server_options: typing.Optional[typing.Union[ServerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37953f1eba9b563d1341cf75bd7d73a57ac96383b9d4bbcb3ad5ab140341b32e(
    *,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    allow_public_subnet: typing.Optional[builtins.bool] = None,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    code_signing_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig] = None,
    current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
    dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment_encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
    filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
    function_name: typing.Optional[builtins.str] = None,
    initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
    layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    profiling: typing.Optional[builtins.bool] = None,
    profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    bundling: typing.Optional[typing.Union[_aws_cdk_aws_lambda_nodejs_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7c1078f47a089ec32759a5895dbdd9baee0042d6d1f2f5014d04a76b084ca0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    site_dir: builtins.str,
    cf_options: typing.Optional[typing.Union[CfOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    errorhtml: typing.Optional[builtins.str] = None,
    indexhtml: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3325321ebadc5e36cd8f3b8ad8b45edb7386a70e17bc2b7a0976fb7ae04ab39e(
    *,
    cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    errorhtml: typing.Optional[builtins.str] = None,
    indexhtml: typing.Optional[builtins.str] = None,
    site_dir: builtins.str,
    cf_options: typing.Optional[typing.Union[CfOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
