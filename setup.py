import setuptools

with open("README.md", "r") as fh:
    long_desctiption = fh.read()

setuptools.setup(
    name="omraidav",
    version="0.0.1",
    author="David Omrai",
    author_email="omraidav@fit.cvut.cz",
    description="Similarity join on two data sets of images",
    long_desctiption=long_desctiption,
    long_desctiption_content_type="text/markdown",
    url="https://gitlab.fit.cvut.cz/omraidav/similarity-join",
    packages=setuptools.find_packages(),
    classifier=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)