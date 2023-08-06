import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='cumulus_kern',  
     version='0.0.1',
     author="BayWa Data Services GmbH",
     author_email="no-reply@baywa-re.com",
     description="Kernel functions for Cumulus",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/nino-baywa/cumulus_kern",
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.8"
 )