import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="digitize",
    version="1.0.0",
    author="LimeGeeg",
    author_email="borovoy06nik@gmail.com",
    description="Break numbers into digits with their names",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LimeGeeg/digitize",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)