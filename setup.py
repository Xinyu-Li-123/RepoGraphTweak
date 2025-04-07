from setuptools import setup, find_packages

with open("requirements-package.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="repograph",
    version="0.1.0",
    packages=find_packages(include=["repograph", "repograph.*"]),
    install_requires=requirements,
    author="Xinyu Li",
    description="A tool to construct code graphs from repositories. Fork from https://github.com/ozyyshr/RepoGraph",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.10',
)
