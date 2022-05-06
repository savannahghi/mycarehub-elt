"""Package setup."""
import subprocess

from setuptools import find_packages, setup

name = "mycarehub-elt"


def get_version():
    """Append git revision to versions, useful for development builds."""
    with open("VERSION") as f:
        versioneer = f.read().strip()

    # Append the Git commit id if this is a development version.
    if versioneer.endswith("+"):
        tag = "v" + versioneer[:-1]
        try:
            desc = subprocess.check_output(
                ["git", "describe", "--match", tag]
            )[:-1].decode()
        except Exception:
            versioneer += "unknown"

        else:
            assert str(desc).startswith(tag)
            import re

            match = re.match(r"v([^-]*)(?:-([0-9]+)-(.*))?$", desc)
            if match is None:  # paranoia
                versioneer += "unknown"
            else:
                ver, rev, local = match.groups()
                ver, rev = ver or "", rev or ""
                local = (local or "").replace("-", ".")

                post = ".post%s+%s" % ((rev, local) if rev else ("", ""))
                versioneer = "%s%s" % (ver, post if rev else "")
                assert "-" not in versioneer

    return versioneer


version = get_version()

with open("README.rst") as readme:
    README = readme.read()

setup(
    name=name,
    version=version,
    packages=find_packages(
        include=['pipelines', 'pipelines.*'],
        exclude=['tests', 'tests.*']),
    description="Mycarehub Datapipeline",
    long_description=README,
    url="https://pip.slade360.co.ke/docs/{}/".format(name),
    author="SIL Developers",
    author_email="developers@savannahinformatics.com",
    license="Proprietary",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: mycarehub",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
    include_package_data=True,
)
