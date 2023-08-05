'''
# CDK Checkov Validator Plugin

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Installation

### TypeScript/JavaScript

```bash
npm install @bridgecrew/cdk-validator-checkov
```

### Python

```bash
pip install cdk-validator-checkov
```

## Usage

To use this plugin in your CDK application add it to the CDK App.

### Python

```python
from cdk_validator_checkov import CheckovValidator

...

App(
  policy_validation_beta1=[
    CheckovValidator()
  ]
)
```

By default, the `CheckovValidator` plugin comes with all `checkov`
[built-in checks for CloudFormation](https://www.checkov.io/5.Policy%20Index/cloudformation.html).
In order to disable any of the checks or just run a subset of them you can use the `check` or `skipCheck` property.

```python
CheckovValidator(
  check= ['CKV_AWS_18', 'CKV_AWS_21']
)
```

```python
CheckovValidator(
  skipCheck= ['CKV_AWS_18', 'CKV_AWS_21']
}
```

### TypeScript

```python
new App({
  policyValidationBeta1: [
    new CheckovValidator(),
  ],
});
```

Specify checks:

```python
new CheckovValidator({
    check: ['CKV_AWS_18', 'CKV_AWS_21'],
});
```

Skip checks:

```python
new CheckovValidator({
    skipCheck: ['CKV_AWS_18', 'CKV_AWS_21'],
});
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


@jsii.implements(_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1)
class CheckovValidator(
    metaclass=jsii.JSIIMeta,
    jsii_type="@bridgecrew/cdk-validator-checkov.CheckovValidator",
):
    '''A validation plugin using checkov.'''

    def __init__(
        self,
        *,
        check: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_check: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param check: List of checks to run. Default: - all checks are run
        :param skip_check: List of checks to skip. Default: - no checks are skipped
        '''
        props = CheckovValidatorProps(check=check, skip_check=skip_check)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="validate")
    def validate(
        self,
        context: _aws_cdk_ceddda9d.IPolicyValidationContextBeta1,
    ) -> _aws_cdk_ceddda9d.PolicyValidationPluginReportBeta1:
        '''The method that will be called by the CDK framework to perform validations.

        This is where the plugin will evaluate the CloudFormation
        templates for compliance and report and violations

        :param context: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e063439c9df87e1026e2e563128a4823309971376880bd39920fea7eab16b80d)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(_aws_cdk_ceddda9d.PolicyValidationPluginReportBeta1, jsii.invoke(self, "validate", [context]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the plugin that will be displayed in the validation report.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="@bridgecrew/cdk-validator-checkov.CheckovValidatorProps",
    jsii_struct_bases=[],
    name_mapping={"check": "check", "skip_check": "skipCheck"},
)
class CheckovValidatorProps:
    def __init__(
        self,
        *,
        check: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_check: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param check: List of checks to run. Default: - all checks are run
        :param skip_check: List of checks to skip. Default: - no checks are skipped
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7806be0626069eea664fb3c72a013643b682ce1c43e7b12ae0660d38e756fb28)
            check_type(argname="argument check", value=check, expected_type=type_hints["check"])
            check_type(argname="argument skip_check", value=skip_check, expected_type=type_hints["skip_check"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if check is not None:
            self._values["check"] = check
        if skip_check is not None:
            self._values["skip_check"] = skip_check

    @builtins.property
    def check(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of checks to run.

        :default: - all checks are run
        '''
        result = self._values.get("check")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def skip_check(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of checks to skip.

        :default: - no checks are skipped
        '''
        result = self._values.get("skip_check")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckovValidatorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CheckovValidator",
    "CheckovValidatorProps",
]

publication.publish()

def _typecheckingstub__e063439c9df87e1026e2e563128a4823309971376880bd39920fea7eab16b80d(
    context: _aws_cdk_ceddda9d.IPolicyValidationContextBeta1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7806be0626069eea664fb3c72a013643b682ce1c43e7b12ae0660d38e756fb28(
    *,
    check: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_check: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
