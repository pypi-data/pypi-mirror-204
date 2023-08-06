from setuptools import find_packages, setup

VERSION = "0.0.3"

setup(
    name="cbmc.py",
    version=VERSION,
    author="ItsRqtl",
    author_email="itsrql@gmail.com",
    description="An unofficial 麥塊匿名發文平台 API wrapper.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ItsRqtl/cbmc.py",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    install_requires=["requests", "aiohttp"],
    python_requires=">=3.6",
)
