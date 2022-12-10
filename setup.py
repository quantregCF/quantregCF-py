from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name="quantregCF",
        version="1.0.0",
        packages=["quantregCF"],
        description="The control function approach for quantile regression models",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/quantregCF/quantregCF-py",
        author="Sokbae (Simon) Lee, Suwijak (Max) Mongkalakorn",
        author_email="sl3841@columbia.edu, sm4791@columbia.edu",
        license="MIT",
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
        ],
        install_requires=[
            "numpy",
            "pandas",
            "scipy",
            "cvxpy"
            ],
        package_dir = {"": "src"}
        )
