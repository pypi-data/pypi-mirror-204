'''
# newrelic-observability-dashboards

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `NewRelic::Observability::Dashboards` v1.1.0.

## Description

CRUD operations for New Relic Dashboards via the NerdGraph API

## References

* [Source](https://github.com/newrelic-experimental/newrelic-cloudformation-resource-providers-dashboards)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name NewRelic::Observability::Dashboards \
  --publisher-id 759f81f13de188bad7cafc8a2d50910f7d5e2bcc \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/759f81f13de188bad7cafc8a2d50910f7d5e2bcc/NewRelic-Observability-Dashboards \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `NewRelic::Observability::Dashboards`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fnewrelic-observability-dashboards+v1.1.0).
* Issues related to `NewRelic::Observability::Dashboards` should be reported to the [publisher](https://github.com/newrelic-experimental/newrelic-cloudformation-resource-providers-dashboards).

## License

Distributed under the Apache-2.0 License.
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
import constructs as _constructs_77d1e7e8


class CfnDashboards(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/newrelic-observability-dashboards.CfnDashboards",
):
    '''A CloudFormation ``NewRelic::Observability::Dashboards``.

    :cloudformationResource: NewRelic::Observability::Dashboards
    :link: https://github.com/newrelic-experimental/newrelic-cloudformation-resource-providers-dashboards
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        dashboard_input: typing.Optional[builtins.str] = None,
        list_query_filter: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        variables: typing.Any = None,
    ) -> None:
        '''Create a new ``NewRelic::Observability::Dashboards``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dashboard_input: 
        :param list_query_filter: 
        :param tags: 
        :param variables: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e95e1c81e5cebb3699baa93ba5fa3ab2a7fe50fff55eea029f7df8749ddf31)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDashboardsProps(
            dashboard_input=dashboard_input,
            list_query_filter=list_query_filter,
            tags=tags,
            variables=variables,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrGuid")
    def attr_guid(self) -> builtins.str:
        '''Attribute ``NewRelic::Observability::Dashboards.Guid``.

        :link: https://github.com/newrelic-experimental/newrelic-cloudformation-resource-providers-dashboards
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrGuid"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnDashboardsProps":
        '''Resource props.'''
        return typing.cast("CfnDashboardsProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-observability-dashboards.CfnDashboardsProps",
    jsii_struct_bases=[],
    name_mapping={
        "dashboard_input": "dashboardInput",
        "list_query_filter": "listQueryFilter",
        "tags": "tags",
        "variables": "variables",
    },
)
class CfnDashboardsProps:
    def __init__(
        self,
        *,
        dashboard_input: typing.Optional[builtins.str] = None,
        list_query_filter: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        variables: typing.Any = None,
    ) -> None:
        '''CRUD operations for New Relic Dashboards via the NerdGraph API.

        :param dashboard_input: 
        :param list_query_filter: 
        :param tags: 
        :param variables: 

        :schema: CfnDashboardsProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8ec58d72d07b15ae7381ca0f66880525b482ca312572db04ef2a9c0fc7fd82b)
            check_type(argname="argument dashboard_input", value=dashboard_input, expected_type=type_hints["dashboard_input"])
            check_type(argname="argument list_query_filter", value=list_query_filter, expected_type=type_hints["list_query_filter"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dashboard_input is not None:
            self._values["dashboard_input"] = dashboard_input
        if list_query_filter is not None:
            self._values["list_query_filter"] = list_query_filter
        if tags is not None:
            self._values["tags"] = tags
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def dashboard_input(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDashboardsProps#DashboardInput
        '''
        result = self._values.get("dashboard_input")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def list_query_filter(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDashboardsProps#ListQueryFilter
        '''
        result = self._values.get("list_query_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''
        :schema: CfnDashboardsProps#Tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def variables(self) -> typing.Any:
        '''
        :schema: CfnDashboardsProps#Variables
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDashboardsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDashboards",
    "CfnDashboardsProps",
]

publication.publish()

def _typecheckingstub__83e95e1c81e5cebb3699baa93ba5fa3ab2a7fe50fff55eea029f7df8749ddf31(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    dashboard_input: typing.Optional[builtins.str] = None,
    list_query_filter: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ec58d72d07b15ae7381ca0f66880525b482ca312572db04ef2a9c0fc7fd82b(
    *,
    dashboard_input: typing.Optional[builtins.str] = None,
    list_query_filter: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass
