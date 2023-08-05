from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'Simple python package for calculating expected outcome of a risk battle'
LONG_DESCRIPTION = 'Simple python package for calculating expected outcome of a risk battle'

# Setting up
setup(
    name="riskCalculator",
    version=VERSION,
    author="Angus Leck",
    author_email="aleck42@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
