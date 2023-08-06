from setuptools import setup, find_packages

setup(
    name="test_mypackage",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib"
    ],
    entry_points={
        "console_scripts": [
            "test_mypackage=mypackage.cli:main"
        ]
    }
)
