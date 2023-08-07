import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "astrojs-aws.construct",
    "version": "0.0.10",
    "description": "The CDK Construct Library of Astro",
    "license": "MIT",
    "url": "https://astro-aws.org/",
    "long_description_content_type": "text/markdown",
    "author": "helbing",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/helbing/astrojs-aws.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "astrojs_aws.construct",
        "astrojs_aws.construct._jsii"
    ],
    "package_data": {
        "astrojs_aws.construct._jsii": [
            "construct@0.0.10.jsii.tgz"
        ],
        "astrojs_aws.construct": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.76.0, <3.0.0",
        "aws-cdk.aws-apigatewayv2-alpha>=2.76.0.a0, <3.0.0",
        "aws-cdk.aws-apigatewayv2-integrations-alpha>=2.76.0.a0, <3.0.0",
        "constructs>=10.2.1, <11.0.0",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
