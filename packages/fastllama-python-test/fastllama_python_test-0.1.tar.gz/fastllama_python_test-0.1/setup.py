import subprocess
from setuptools import setup, find_packages, Command

# # Read requirements.txt
# with open("requirements.txt") as f:
#     requirements = f.read().splitlines()

setup(
    name="fastllama_python_test",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy==1.24.2",
        "sentencepiece==0.1.97",
        "torch==2.0.0",
        "py-cpuinfo==9.0.0",
        "inquirer==3.1.3",
        "transformers",
        "peft"
    ],
    entry_points={
        "console_scripts": [
            "build_fastllama=build_python:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)