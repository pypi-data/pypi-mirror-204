from setuptools import setup, find_packages

setup(
    name="TPLUtils",
    version="0.0.2a'",
    packages=find_packages(where="src"),
    description='A package used for the TPL project',
    license='MIT',
    install_requires=[
        "fastapi",
        "firebase-admin",
        "google",
        "pydantic",
    ],
    package_dir={'': 'src'},
    url="https://github.com/The-Programming-Lab/TPL_package",
    author="The Programming Lab",
    author_email="braeden.norman6@gmail.com"
)