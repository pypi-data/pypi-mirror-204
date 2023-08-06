from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required_packages = f.read().splitlines()

setup(
    name="winavsos",
    version="0.0.0.2",
    packages=find_packages(),
    install_requires=required_packages,
    description="An Automated Vulnerabilty Scanner",
    author="Tomiwa Ibikunle",
    author_email="tomzy2506@gmail.com",
    license="MIT License",
    url="https://github.com/Tomzy2506/AVSOS",
    package_data={
    	"winavsos": ["config.ini", "service-names-port-numbers.csv", "amass.exe"],
    	},
    entry_points={
        "console_scripts": [
            "winavsos=winavsos.main:main",
        ],
    },
)
