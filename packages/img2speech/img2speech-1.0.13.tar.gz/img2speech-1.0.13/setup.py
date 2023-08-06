import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="img2speech",  # This is the name of the package
    version="1.0.13",  # The initial release version
    author="Shreyas P J",  # Full name of the author
    description="Integrated Python package for converting Image to speech",
    long_description=long_description,  # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),  # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # Information to filter the project on PyPi website
    python_requires='>=3.8',  # Minimum version requirement of the package
    py_modules=["img2speech"],  # Name of the python package
    package_dir={'': 'img2speech/src'},  # Directory of the source code of the package
    install_requires=['easyocr==1.6.2', 'gtts==2.3.1', 'langdetect==1.0.9','pypdfium2==4.5.0']
    # Install other dependencies if any
)
