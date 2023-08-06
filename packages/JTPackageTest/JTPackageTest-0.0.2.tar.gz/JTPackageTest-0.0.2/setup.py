from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Testing module functionality and package creation'
LONG_DESCRIPTION = 'Testing module functionality and package creation'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="JTPackageTest", 
        version=VERSION,
        author="Joshua Taylor",
        author_email="joshua.taylor@integer-tech.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['opencv-python'], # add any additional packages that 
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