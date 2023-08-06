import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="omglinegraphs",
    version="0.1.0",
    author="OmgRod",
    description="A package for creating line graphs with units and labels",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0mgRod/linegraph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy>=1.19.5",
        "matplotlib>=3.4.2",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.4",
            "flake8>=3.9.2",
            "mypy>=0.910",
            "coverage>=5.5",
        ]
    },
    entry_points={
        "console_scripts": [
            "linegraph=linegraph.cli:main",
        ],
    },
)
