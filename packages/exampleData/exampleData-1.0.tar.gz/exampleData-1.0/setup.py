from setuptools import setup, find_packages

setup(
    name="exampleData",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "requests"
    ],
    author="NCQH",
    author_email="ncquochuy21@gmail.com",
    description="Package for example data for numerical study",
    long_description_content_type="text/markdown",
    url="https://github.com/NCQH/exampleData",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)