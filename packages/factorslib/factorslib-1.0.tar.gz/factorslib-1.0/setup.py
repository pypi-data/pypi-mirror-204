# setup.py

import setuptools
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="factorslib",
    version="1.0",
    author="wytxty",
    author_email="yvettewkkaa@gmail.com",
    description="financial factors calculation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wytxty/factorslib",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords="codepay, codepay_python")