from setuptools import setup, find_packages

setup(
    name="TPLUtils",
    version="0.0.1",
    packages=find_packages(exclude=['tests*']),
    description='A package used for the TPL project',
    license='MIT',
    install_requires=[
        "fastapi",
        "firebase-admin",
        "google",
        "pydantic",
    ],
    url="https://github.com/The-Programming-Lab/TPL_package",
    author="The Programming Lab",
    author_email="braeden.norman6@gmail.com"
)