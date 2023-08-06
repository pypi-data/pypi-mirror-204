from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="jnb2py",
    version="0.0.2",
    description="Converts .ipynb files to .py files.",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/subhranil2605/nb2py",
    author="Subhranil Sarkar",
    author_email="subhranil2605@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10"
)
