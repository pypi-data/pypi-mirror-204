from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required_packages = f.read().splitlines()

classifiers = {
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Linux",
    }
    
"Homepage" == "https://github.com/Tomzy2506/AVSOS"

setup(
    name="avsos",
    version="0.0.8",
    description = "An automated Vulnerability Scanner",
    readme = "README.md",
    packages=find_packages(),
    package_data={
        "avsos": ["config.ini", "service-names-port-numbers.csv"]
    },
    install_requires=required_packages,
    entry_points={
        "console_scripts": [
            "avsos=avsos.main:main",
        ],
    },
    
)
