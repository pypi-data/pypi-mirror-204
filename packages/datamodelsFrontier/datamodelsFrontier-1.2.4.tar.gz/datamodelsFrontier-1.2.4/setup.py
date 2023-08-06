from setuptools import setup
import os

# Open readme when package starts
with open("pypi-description.md", "r") as fh:
    long_description = fh.read()

# Read the version number from the environment variable
version = os.getenv('PACKAGE_VERSION', '0.0.0')

# Dependencies
extra_test = [
    'pytest>=4',
    'pytest-cov>=2',
]

setup(
    name='datamodelsFrontier',
    version=version,
    description="Datamodels needed for Frontier API",

    author='THG-Frontier',
    author_email='DL-TechAPIGateway@thehutgroup.com',

    install_requires=['pydantic', ],
    extras_require={
        'dev': extra_test
    },

    py_modules=['downstream, external'],
    package_dir={"": "src"},

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],

    long_description=long_description,
    long_description_content_type="text/markdown",
)
