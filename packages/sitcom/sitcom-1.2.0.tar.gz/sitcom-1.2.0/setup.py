from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name='sitcom',
    version='1.2.0',
    packages=['sitcom'],
    url='https://github.com/pu3/SITCoM',
    license='LICENSE',
    author='Purvi Udhwani, Arpit Shrivastava, Ritesh Patel',
    author_email='purviaries@aries.res.in,arpits@aries.res.in,ritesh.sophy@gmail.com',
    description='SITCoM: SiRGraF Integrated Tool for Coronal dynaMics',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',
    install_requires=[
        'PyQt5','opencv-python','numpy','matplotlib','scikit-image','sunpy','astropy'
    ],
    package_dir={'sitcom': 'sitcom'},
    package_data={'sitcom': ['data/*','icon/*','load/*','font/*']}
)
