import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my-pipeline-package",
    version="1.1.2",
    description="Build package from python tests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=True,
)
