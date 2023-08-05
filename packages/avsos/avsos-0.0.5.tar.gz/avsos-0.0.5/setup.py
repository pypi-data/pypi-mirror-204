from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required_packages = f.read().splitlines()

setup(
    name="avsos",
    version="0.0.5",
    packages=find_packages(),
    package_data={
        "avsos": ["config.ini"]
    },
    install_requires=required_packages,
    entry_points={
        "console_scripts": [
            "avsos=avsos.main:main",
        ],
    },
)
