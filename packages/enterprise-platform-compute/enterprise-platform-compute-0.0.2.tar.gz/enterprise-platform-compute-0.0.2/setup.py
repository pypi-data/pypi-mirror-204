import setuptools

setuptools.setup(
    name="enterprise-platform-compute",
    version="0.0.2",
    packages=["compute"],
    install_requires=[
        "cloudpickle==2.2.1",
        "gql[botocore,requests]==3.4.0",
        "httpx==0.24.0",
        "networkx==3.1",
        "polling2==0.5.0",
        "websockets==11.0.2",
    ],
)
