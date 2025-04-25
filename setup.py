from setuptools import setup, find_packages

setup(
    name="edge-aws-system",
    version="0.1.0",
    packages=find_packages(include=['src*']),
    install_requires=[
        "paho-mqtt",
        "pyarrow",
        "boto3",
        "pandas",
        "aiohttp",
        "python-dotenv"
    ]
) 