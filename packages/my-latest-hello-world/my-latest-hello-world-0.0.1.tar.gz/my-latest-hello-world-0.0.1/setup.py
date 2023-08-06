from setuptools import setup, find_packages

with open("./requirements.txt", "r", encoding="utf-8") as reqs_file:
    reqs = reqs_file.readlines()

setup(
    name="my-latest-hello-world",
    version="0.0.1",
    description="A simple library to print hello world",
    long_description=open("README.rst", encoding="utf-8").read(),
    author="Pragyat Singh Rana",
    packages=find_packages(),
    install_requires=reqs,
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
