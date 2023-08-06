import subprocess

import setuptools

try:
    import pypandoc

    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()


def get_tag():
    tag = subprocess.getoutput('git tag --sort=version:refname | tail -n1')
    commits = subprocess.getoutput(f'git rev-list {tag}..HEAD --count')
    return f'{tag}.{commits}'


setuptools.setup(
    name="data-watch-sdk",
    version="0.0.1b1",
    author="Algora Labs",
    author_email="hello@algoralabs.com",
    description="Data Watch Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://alpha.dev",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7",
    packages=setuptools.find_packages(
        include=['data_watch*'],
        exclude=['tests.*']
    ),
    install_requires=[
        "requests==2.28.1",
        "pandas==1.3.5",
        "cachetools==5.2.0",
        "pydash==5.1.0",
        "PyYaml==6.0",
        "asyncio==3.4.3",
        "aiohttp==3.8.1",
        "ujson==5.4.0",
        "msgpack==1.0.4",
        "fastparquet==0.8.1",
        "scipy==1.8.0",
        "duckdb==0.7.1",
        "pydantic==1.9.1",
        "aiocache==0.11.1"
    ]
)
