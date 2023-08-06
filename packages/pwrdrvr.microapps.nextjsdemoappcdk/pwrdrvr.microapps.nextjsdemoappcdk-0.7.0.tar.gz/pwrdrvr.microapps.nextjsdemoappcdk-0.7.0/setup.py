import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "pwrdrvr.microapps.nextjsdemoappcdk",
    "version": "0.7.0",
    "description": "Release app for the MicroApps framework, by PwrDrvr LLC. Provides the ability to control which version of an app is launched.",
    "license": "MIT",
    "url": "https://github.com/pwrdrvr/microapps-app-nextjs-demo",
    "long_description_content_type": "text/markdown",
    "author": "PwrDrvr LLC",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/pwrdrvr/microapps-app-nextjs-demo"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "pwrdrvr.microapps.nextjsdemoappcdk",
        "pwrdrvr.microapps.nextjsdemoappcdk._jsii"
    ],
    "package_data": {
        "pwrdrvr.microapps.nextjsdemoappcdk._jsii": [
            "microapps-app-nextjs-demo-cdk@0.7.0.jsii.tgz"
        ],
        "pwrdrvr.microapps.nextjsdemoappcdk": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk-lib>=2.24.1, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.52.1, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
