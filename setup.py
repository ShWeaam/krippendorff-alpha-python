"""
Setup script for Krippendorff Alpha package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="krippendorff-alpha",
    version="1.0.0",
    author="Weaam Shaheen",
    author_email="weaam.2511@gmail.com",
    description="Comprehensive implementation of Krippendorff's Alpha for inter-rater reliability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ShWeaam/krippendorff-alpha-python-calculator",
    project_urls={
        "Bug Tracker": "https://github.com/ShWeaam/krippendorff-alpha-python-calculator/issues",
        "Documentation": "https://github.com/ShWeaam/krippendorff-alpha-python-calculator#readme",
        "Source Code": "https://github.com/ShWeaam/krippendorff-alpha-python-calculator",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Sociology",
        "Topic :: Text Processing :: Linguistic",
    ],
    package_dir={"": "."},
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
            "sphinx",
            "sphinx-rtd-theme",
        ],
        "web": [
            "streamlit>=1.28.0",
            "plotly>=5.0.0",
            "fastapi>=0.104.0",
            "uvicorn>=0.24.0",
        ],
        "all": [
            "scipy>=1.7.0",
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "krippendorff-alpha=krippendorff_alpha.cli:main",
        ],
    },
    keywords=[
        "krippendorff", "alpha", "inter-rater", "reliability", "agreement", 
        "statistics", "content-analysis", "research", "data-science"
    ],
    include_package_data=True,
    zip_safe=False,
)