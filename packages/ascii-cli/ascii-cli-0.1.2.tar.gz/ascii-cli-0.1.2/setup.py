from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="ascii-cli",
    author="mrq-andras",
    version="0.1.2",
    packages=find_packages(),
    package_data={'src': ['func.py']},
    install_requires=["Pillow"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    entry_points={
        "console_scripts": [
            "ascii-cli=src.__main__:main"
        ]
    },
    python_requires=">=3.6",
    url="https://github.com/mrq-andras/ascii-cli",
    license="MIT",
    description="A command-line tool that converts images to ASCII art.",
)
