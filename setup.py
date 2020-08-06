import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tinytcp",
    version="1.0.0",
    license='MIT',
    author="Mohammed Boukhlouf",
    author_email="mohammed.boukhlouf@outlook.com",
    description="Event based package for tcp server/client on top of python sockets package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/M-Boukhlouf/tinytcp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)