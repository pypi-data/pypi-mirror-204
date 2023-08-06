import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='dedscumulus',  
     version='0.0.3',
     author="BayWa r.e. Data Services GmbH",
     author_email="no-reply@baywa-re.com",
     description="Kernel functions for Cumulus",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/nino-baywa/dedscumulus",
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
    package_dir = {"src": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.8"
 )