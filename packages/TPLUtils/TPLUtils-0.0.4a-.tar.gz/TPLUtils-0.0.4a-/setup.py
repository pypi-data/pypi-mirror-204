from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
    
setup(
    name="TPLUtils",
    version="0.0.4a'",
    packages=find_packages(where="src"),
    description='A package used for the TPL project',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
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