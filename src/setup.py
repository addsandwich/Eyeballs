from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'The Eyeballs Python Package'
LONG_DESCRIPTION = 'The Eyeballs python package is designed to simplify image transfer in python'

# Setting up
setup(
    name="Eyeballs",
    version=VERSION,
    author="Christopher J. Watson",
    author_email="<Christopher.Joseph.Watson@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)