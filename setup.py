import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="emgw_trigger_strat",
    version="0.0.1",
    author="Viraj Karambelkar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="astronomy image mma ligo",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires='>=3.8',
    install_requires=[
        "astropy",
        "pickle",
        "numpy",
        "pandas",
        "glob",
        "gwemlightcurves",
        "flask_wtf",
        "flask_restful",
        "wtforms",
        "sys",
        "datetime",
        "os",
        "flask"
    ],
)
