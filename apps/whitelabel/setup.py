import re
from setuptools import setup, find_packages

# read requirements
with open("requirements.txt") as f:
    install_requires = [line.strip() for line in f if line.strip()]

# extract __version__ without importing the module
_version_re = re.compile(r"__version__\s*=\s*['\"]([^'\"]+)['\"]")
with open("whitelabel/__init__.py", "r", encoding="utf-8") as f:
    content = f.read()
match = _version_re.search(content)
if not match:
    raise RuntimeError("Unable to find version string in whitelabel/__init__.py")
version = match.group(1)

setup(
    name="whitelabel",
    version=version,
    description="ERPNext Whitelabel",
    author="Bhavesh Maheshwari",
    author_email="maheshwaribhavesh95863@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
)
