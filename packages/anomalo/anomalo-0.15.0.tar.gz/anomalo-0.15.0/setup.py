import re

from setuptools import find_packages, setup


def get_version():
    try:
        f = open(f"anomalo/_version.py")
    except OSError:
        return None
    for line in f.readlines():
        mo = re.match('__version__ = "([^\']+)"', line)
        if mo:
            ver = mo.group(1)
            return ver
    return None


setup(
    name="anomalo",
    version=get_version(),
    description="Python bindings for the Anomalo API",
    long_description="A basic REST API client and command line client for Anomalo",
    url="https://anomalo.com",
    author="Anomalo",
    author_email="support@anomalo.com",
    license="license.txt",
    package=find_packages(),
    install_requires=["requests", "fire"],
    tests_require=[],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "anomalo = anomalo:anomalo.main",
        ]
    },
    extras_require={"yaml": ["pyyaml>=5.2"]},
)
