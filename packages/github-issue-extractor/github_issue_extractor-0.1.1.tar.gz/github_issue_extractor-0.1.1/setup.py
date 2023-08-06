import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="github_issue_extractor",
    version="0.1.1",
    author="Sudarshan Sinha",
    author_email="s.sinha2103@outlook.com",
    description="GitHubIssueExtractor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ssinha2103/github-issues_to_excel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "setuptools",
        "requests",
        "openpyxl"
    ]
)
