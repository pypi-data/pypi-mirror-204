import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymwr",
    version="0.1.0",
    author="Imran Sayyed, Hamid Ali Syed",
    author_email="sayyed950@gmail.com, hamidsyed37@gmail.com",
    description="Python package to interact with MWR data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imsayyed/pymwr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
