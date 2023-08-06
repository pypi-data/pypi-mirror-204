import setuptools

setuptools.setup(
    name="github_issue_extractor",
    version="0.1.0",
    author="Sudarshan Sinha",
    author_email="s.sinha2103@outlook.com",
    description="GitHubIssueExtractor",
    long_description="GitHubIssueExtractor",
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
