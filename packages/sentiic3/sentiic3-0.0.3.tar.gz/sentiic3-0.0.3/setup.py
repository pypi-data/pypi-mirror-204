from setuptools import setup
from distutils.core import setup
setup(
    name = "sentiic3",
    version= "0.0.3",
    description= " Sentimental Analysis From Social Media",
    author="DUMPA NAVEEN KUMAR REDDY",
    author_email="naveenkumarreddydumpa@gmail.com",
    py_modules=["sentiic3"],
    package_dir={"":"src"},
    include_package_data=True,
)
