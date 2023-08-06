import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-cloudformation-unxpose-iam-integration-module",
    "version": "1.0.0.a7",
    "description": "Schema for Module Fragment of type Unxpose::IAM::Integration::MODULE",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/cdk-cloudformation.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-cloudformation.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_cloudformation_unxpose_iam_integration_module",
        "cdk_cloudformation_unxpose_iam_integration_module._jsii"
    ],
    "package_data": {
        "cdk_cloudformation_unxpose_iam_integration_module._jsii": [
            "unxpose-iam-integration-module@1.0.0-alpha.7.jsii.tgz"
        ],
        "cdk_cloudformation_unxpose_iam_integration_module": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.72.1, <3.0.0",
        "constructs>=10.1.302, <11.0.0",
        "jsii>=1.80.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
