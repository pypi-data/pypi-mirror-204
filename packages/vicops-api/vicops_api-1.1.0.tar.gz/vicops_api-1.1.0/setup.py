import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vicops_api",
    author="artegoser",
    description="python api wrapper for vicops2",
    keywords="api, wrapper, vicops",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/ERTH2/vicops-api-py",
    project_urls={
        "Source Code": "https://github.com/ERTH2/vicops-api-py",
    },
    version="1.1.0",
    packages=["vicops_api"],
    python_requires=">=3.10",
    install_requires=["requests"],
)
