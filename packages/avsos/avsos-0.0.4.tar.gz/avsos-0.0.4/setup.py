from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required_packages = f.read().splitlines()

setup(
    name="avsos",
    version="0.0.4",
    packages=find_packages(),
    install_requires=required_packages,
    entry_points={
        "console_scripts": [
            "avsos=avsos.main:main",
        ],
    },
)
