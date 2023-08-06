from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="vanitas-py",
    version="0.5",
    description="vanitas API wrapper",
    py_modules=["vanitas"],
    package_dir={'': 'vanitas'},
    install_requires=["requests", "typing"],
    extras_require={
                      "dev":[
                          "pytest",
                      ],},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Moezilla/vanitas-Py",
    author="Nksamax"

)
