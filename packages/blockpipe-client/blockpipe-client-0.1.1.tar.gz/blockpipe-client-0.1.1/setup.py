from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="blockpipe-client",
    version="0.1.1",
    author="blockpipe.io",
    author_email="support@blockpipe.io",
    description="A Python library for interacting with Blockpipe Endpoint API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blockpipe/python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6",
    install_requires=["requests"],
)
