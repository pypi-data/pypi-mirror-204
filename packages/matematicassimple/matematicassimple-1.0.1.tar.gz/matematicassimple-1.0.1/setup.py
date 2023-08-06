import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="matematicassimple",
    version="1.0.1",
    scripts=["__init__.py"],
    description="Un paquete para usar algo matematico de forma sencilla",
    long_description=long_description,
    packages=setuptools.find_packages(),
    license='MIT',
    long_description_content_type="text/markdown",
    url="https://github.com/Aldogamer01/matematicassimple",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)