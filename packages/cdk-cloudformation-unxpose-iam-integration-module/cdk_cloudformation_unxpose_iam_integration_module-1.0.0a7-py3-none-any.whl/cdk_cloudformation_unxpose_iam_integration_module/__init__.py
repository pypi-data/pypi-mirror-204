'''
# unxpose-iam-integration-module

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Unxpose::IAM::Integration::MODULE` v1.0.0.

## Description

Schema for Module Fragment of type Unxpose::IAM::Integration::MODULE

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Unxpose::IAM::Integration::MODULE \
  --publisher-id 8f866e0a9c638d58c2b4c9ef8507be596497629e \
  --type MODULE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/module/8f866e0a9c638d58c2b4c9ef8507be596497629e/Unxpose-IAM-Integration-MODULE \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Unxpose::IAM::Integration::MODULE`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Funxpose-iam-integration-module+v1.0.0).
* Issues related to `Unxpose::IAM::Integration::MODULE` should be reported to the [publisher](undefined).

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


class CfnIntegrationModule(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/unxpose-iam-integration-module.CfnIntegrationModule",
):
    '''A CloudFormation ``Unxpose::IAM::Integration::MODULE``.

    :cloudformationResource: Unxpose::IAM::Integration::MODULE
    :link: http://unknown-url
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        parameters: typing.Optional[typing.Union["CfnIntegrationModulePropsParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        resources: typing.Optional[typing.Union["CfnIntegrationModulePropsResources", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Create a new ``Unxpose::IAM::Integration::MODULE``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param parameters: 
        :param resources: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e007634bd28c31434790d2267792872f19c4eb0a079e63e0ff87fe468940bd5f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnIntegrationModuleProps(parameters=parameters, resources=resources)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnIntegrationModuleProps":
        '''Resource props.'''
        return typing.cast("CfnIntegrationModuleProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/unxpose-iam-integration-module.CfnIntegrationModuleProps",
    jsii_struct_bases=[],
    name_mapping={"parameters": "parameters", "resources": "resources"},
)
class CfnIntegrationModuleProps:
    def __init__(
        self,
        *,
        parameters: typing.Optional[typing.Union["CfnIntegrationModulePropsParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        resources: typing.Optional[typing.Union["CfnIntegrationModulePropsResources", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Schema for Module Fragment of type Unxpose::IAM::Integration::MODULE.

        :param parameters: 
        :param resources: 

        :schema: CfnIntegrationModuleProps
        '''
        if isinstance(parameters, dict):
            parameters = CfnIntegrationModulePropsParameters(**parameters)
        if isinstance(resources, dict):
            resources = CfnIntegrationModulePropsResources(**resources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f589e4d90afc06bb77b44b025b8d083391c3df3cea270ecb2eafccd7fed0d8f5)
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parameters is not None:
            self._values["parameters"] = parameters
        if resources is not None:
            self._values["resources"] = resources

    @builtins.property
    def parameters(self) -> typing.Optional["CfnIntegrationModulePropsParameters"]:
        '''
        :schema: CfnIntegrationModuleProps#Parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional["CfnIntegrationModulePropsParameters"], result)

    @builtins.property
    def resources(self) -> typing.Optional["CfnIntegrationModulePropsResources"]:
        '''
        :schema: CfnIntegrationModuleProps#Resources
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional["CfnIntegrationModulePropsResources"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationModuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/unxpose-iam-integration-module.CfnIntegrationModulePropsParameters",
    jsii_struct_bases=[],
    name_mapping={"external_id": "externalId"},
)
class CfnIntegrationModulePropsParameters:
    def __init__(
        self,
        *,
        external_id: typing.Optional[typing.Union["CfnIntegrationModulePropsParametersExternalId", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param external_id: ExternalId.

        :schema: CfnIntegrationModulePropsParameters
        '''
        if isinstance(external_id, dict):
            external_id = CfnIntegrationModulePropsParametersExternalId(**external_id)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e75cc9571c88d3b597e2411658f00550e61db785b11300bcd2214c5b2849e9e)
            check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_id is not None:
            self._values["external_id"] = external_id

    @builtins.property
    def external_id(
        self,
    ) -> typing.Optional["CfnIntegrationModulePropsParametersExternalId"]:
        '''ExternalId.

        :schema: CfnIntegrationModulePropsParameters#ExternalId
        '''
        result = self._values.get("external_id")
        return typing.cast(typing.Optional["CfnIntegrationModulePropsParametersExternalId"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationModulePropsParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/unxpose-iam-integration-module.CfnIntegrationModulePropsParametersExternalId",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnIntegrationModulePropsParametersExternalId:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''ExternalId.

        :param description: 
        :param type: 

        :schema: CfnIntegrationModulePropsParametersExternalId
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1279ac23eeda775923af6341b135e46a5d160d3b8f55436540d73820cfc77cac)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnIntegrationModulePropsParametersExternalId#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnIntegrationModulePropsParametersExternalId#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationModulePropsParametersExternalId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/unxpose-iam-integration-module.CfnIntegrationModulePropsResources",
    jsii_struct_bases=[],
    name_mapping={"unxpose_policy": "unxposePolicy", "unxpose_role": "unxposeRole"},
)
class CfnIntegrationModulePropsResources:
    def __init__(
        self,
        *,
        unxpose_policy: typing.Optional[typing.Union["CfnIntegrationModulePropsResourcesUnxposePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        unxpose_role: typing.Optional[typing.Union["CfnIntegrationModulePropsResourcesUnxposeRole", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param unxpose_policy: 
        :param unxpose_role: 

        :schema: CfnIntegrationModulePropsResources
        '''
        if isinstance(unxpose_policy, dict):
            unxpose_policy = CfnIntegrationModulePropsResourcesUnxposePolicy(**unxpose_policy)
        if isinstance(unxpose_role, dict):
            unxpose_role = CfnIntegrationModulePropsResourcesUnxposeRole(**unxpose_role)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ca08dc9374092b77f3e2462f88d86c15ec638f3ca898f12587f76db702ab52)
            check_type(argname="argument unxpose_policy", value=unxpose_policy, expected_type=type_hints["unxpose_policy"])
            check_type(argname="argument unxpose_role", value=unxpose_role, expected_type=type_hints["unxpose_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if unxpose_policy is not None:
            self._values["unxpose_policy"] = unxpose_policy
        if unxpose_role is not None:
            self._values["unxpose_role"] = unxpose_role

    @builtins.property
    def unxpose_policy(
        self,
    ) -> typing.Optional["CfnIntegrationModulePropsResourcesUnxposePolicy"]:
        '''
        :schema: CfnIntegrationModulePropsResources#UnxposePolicy
        '''
        result = self._values.get("unxpose_policy")
        return typing.cast(typing.Optional["CfnIntegrationModulePropsResourcesUnxposePolicy"], result)

    @builtins.property
    def unxpose_role(
        self,
    ) -> typing.Optional["CfnIntegrationModulePropsResourcesUnxposeRole"]:
        '''
        :schema: CfnIntegrationModulePropsResources#UnxposeRole
        '''
        result = self._values.get("unxpose_role")
        return typing.cast(typing.Optional["CfnIntegrationModulePropsResourcesUnxposeRole"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationModulePropsResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/unxpose-iam-integration-module.CfnIntegrationModulePropsResourcesUnxposePolicy",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnIntegrationModulePropsResourcesUnxposePolicy:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnIntegrationModulePropsResourcesUnxposePolicy
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b5edd81ee288f35fa2ebe96875365b97e71d951ea5ed5f3543b533dfbf855c)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnIntegrationModulePropsResourcesUnxposePolicy#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnIntegrationModulePropsResourcesUnxposePolicy#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationModulePropsResourcesUnxposePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/unxpose-iam-integration-module.CfnIntegrationModulePropsResourcesUnxposeRole",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnIntegrationModulePropsResourcesUnxposeRole:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnIntegrationModulePropsResourcesUnxposeRole
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b5abd3bd4fe0297c0b55df2ef4d4d895e428fd5c943e110a98c3bd49c2cd75e)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnIntegrationModulePropsResourcesUnxposeRole#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnIntegrationModulePropsResourcesUnxposeRole#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationModulePropsResourcesUnxposeRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnIntegrationModule",
    "CfnIntegrationModuleProps",
    "CfnIntegrationModulePropsParameters",
    "CfnIntegrationModulePropsParametersExternalId",
    "CfnIntegrationModulePropsResources",
    "CfnIntegrationModulePropsResourcesUnxposePolicy",
    "CfnIntegrationModulePropsResourcesUnxposeRole",
]

publication.publish()

def _typecheckingstub__e007634bd28c31434790d2267792872f19c4eb0a079e63e0ff87fe468940bd5f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    parameters: typing.Optional[typing.Union[CfnIntegrationModulePropsParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    resources: typing.Optional[typing.Union[CfnIntegrationModulePropsResources, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f589e4d90afc06bb77b44b025b8d083391c3df3cea270ecb2eafccd7fed0d8f5(
    *,
    parameters: typing.Optional[typing.Union[CfnIntegrationModulePropsParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    resources: typing.Optional[typing.Union[CfnIntegrationModulePropsResources, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e75cc9571c88d3b597e2411658f00550e61db785b11300bcd2214c5b2849e9e(
    *,
    external_id: typing.Optional[typing.Union[CfnIntegrationModulePropsParametersExternalId, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1279ac23eeda775923af6341b135e46a5d160d3b8f55436540d73820cfc77cac(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ca08dc9374092b77f3e2462f88d86c15ec638f3ca898f12587f76db702ab52(
    *,
    unxpose_policy: typing.Optional[typing.Union[CfnIntegrationModulePropsResourcesUnxposePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    unxpose_role: typing.Optional[typing.Union[CfnIntegrationModulePropsResourcesUnxposeRole, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b5edd81ee288f35fa2ebe96875365b97e71d951ea5ed5f3543b533dfbf855c(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5abd3bd4fe0297c0b55df2ef4d4d895e428fd5c943e110a98c3bd49c2cd75e(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
