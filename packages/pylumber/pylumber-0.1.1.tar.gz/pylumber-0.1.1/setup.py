from setuptools import setup, find_packages

VERSION = '0.1.1'
DESCRIPTION = 'Lumberjack for your Code, Logs, Prints, Errors and more.'
LONG_DESCRIPTION = 'pyLumber is a Python library for logging and debugging. It is designed to be simple and easy to use.'

setup(
    name="pylumber",
    version=VERSION,
    author="Tim Yang (TimMUP)",
    author_email="thryang@outlook.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'logging', 'debugging', 'lumberjack'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)
