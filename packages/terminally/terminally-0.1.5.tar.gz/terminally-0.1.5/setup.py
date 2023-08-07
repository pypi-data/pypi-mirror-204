from setuptools import setup, find_packages

setup(
    name="terminally",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        "appdirs",
        "openai"
    ],
    entry_points={
        "console_scripts": [
            "ally=terminally.ally:main",
        ],
    },
)