from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dejankify",
    version="0.1.1",
    author="Josh Wren",
    author_email="joshisplutar@gmail.com",
    description="A tool to help you find and remove unused imports in your python project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoshCLWren/dejankify",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.11",
    install_requires=[
        "pip",
        "setuptools",
        "wheel",
        "pdbpp",
        "black",
        "flake8",
        "isort",
        "pylint",
        "pydocstyle",
        "mypy",
        "fancycompleter",
        "click",
        "typing-extensions",
        "astroid",
        "dill",
        "mccabe",
        "tomlkit",
        "pytest",
        "argparse",
        "pluggy",
        "iniconfig",
        "attrs"
    ],
    entry_points={
        "console_scripts": [
            "dejankify=dejankify.dependency_cleanup:parse_and_start",
        ],
    },
)