from setuptools import setup, find_packages
import os
import versioneer

PACKAGE_NAME = "frigate"
HERE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(HERE, "README.md"), encoding="utf8").read()

PACKAGES = find_packages(
    exclude=["tests", "tests.*", "modules", "modules.*", "docs", "docs.*"]
)


# For now we simply define the install_requires based on the contents
# of requirements.txt. In the future, install_requires may become much
# looser than the (automatically) resolved requirements.txt.
with open(os.path.join(HERE, "requirements.txt"), "r") as fh:
    REQUIRES = [line.strip() for line in fh]

if "GIT_DESCRIBE_TAG" in os.environ:
    version = os.environ["GIT_DESCRIBE_TAG"] + os.environ.get("VERSION_SUFFIX", "")
else:
    version = versioneer.get_version()

setup(
    name=PACKAGE_NAME,
    version=version,
    license="Apache License 2.0",
    url="",
    download_url="",
    author="Jacob Tomlinson",
    author_email="jtomlinson@nvidia.com",
    description="A tool for autogenerating helm documentation.",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=REQUIRES,
    cmdclass=versioneer.get_cmdclass(),
    entry_points={"console_scripts": ["frigate = frigate.cli:cli"]},
)
