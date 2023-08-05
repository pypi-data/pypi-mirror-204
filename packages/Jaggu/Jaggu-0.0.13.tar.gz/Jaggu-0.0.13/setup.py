from setuptools import setup, find_packages


VERSION = '0.0.13'
DESCRIPTION = 'Lulu'
LONG_DESCRIPTION = 'Lulu'

# Setting up
setup(
    name="Jaggu",
    version=VERSION,
    author="Anonymous",
    author_email="mohammedfaisal3366@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)