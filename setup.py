from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip()]

setup(
    name="arxiv-summarizer",
    version="1.0.0",
    author="",
    description="A Python application that downloads academic papers from arXiv and generates summaries using AI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/user-attachments/arxiv-summarizer",
    package_dir={"": "."},
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "arxiv-summarizer=main:main",
        ],
    },
)