from setuptools import find_packages, setup

__version__ = "0.1.0-beta.1"

install_requires = [
    "pydantic>=1.10.7",
    "requests>=2.28.2",
    "tiktoken>=0.3.3",
]

extras_require = {
    "dev": [
        "pre-commit>=3.2.1",
        "pytest>=7.2.2",
        "responses>=0.23.1",
    ],
    "docs": [
        "mkdocs>=1.4.2",
        "mkdocstrings>=0.20.0",
        "mkdocs-material>=9.1.4",
    ],
}

extras_require["all"] = extras_require["dev"] + extras_require["docs"]

setup(
    name="lmao-nlp",
    version=__version__,
    description="LMAO: Language Model Adapters and Orchestrators",
    author="Johnny Greco",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require=extras_require,
    url="https://github.com/johnnygreco/lmao",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
