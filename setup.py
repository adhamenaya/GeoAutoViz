from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'GeoAutoViz'
LONG_DESCRIPTION = 'A software package for automating geospatial data analytics and visualization'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="GeoAutoViz",
    version=VERSION,
    author="Adham Enaya",
    author_email="adhamenaya@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[], # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['geospatial', 'analytics', 'visualization'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)