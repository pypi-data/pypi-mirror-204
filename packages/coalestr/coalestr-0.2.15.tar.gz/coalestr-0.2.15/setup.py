from setuptools import setup, find_packages

VERSION = '0.2.15' 
DESCRIPTION = 'Short description of coalestr'
LONG_DESCRIPTION = 'Long description of coalestr'

# Setting up
setup(
       # the name must match the folder name'
        name="coalestr", 
        version=VERSION,
        author="Dominic Kwiatkowski",
        author_email="<dkwiatkowski@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)