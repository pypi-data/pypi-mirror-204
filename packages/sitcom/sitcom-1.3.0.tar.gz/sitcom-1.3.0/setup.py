from setuptools import setup

setup(
    name='sitcom',
    version='1.3.0',
    packages=['sitcom'],
    url='https://github.com/pu3/SITCoM',
    license='LICENSE',
    author='Purvi Udhwani',
    author_email='purviaries@aries.res.in',
    description='SITCoM: SiRGraF Integrated Tool for Coronal dynaMics',
    install_requires=[
        'PyQt5','opencv-python','numpy','matplotlib','scikit-image','sunpy','astropy'
    ],
    package_dir={'sitcom': 'sitcom'},
    package_data={'sitcom': ['data/*','icon/*','load/*','font/*']}
)
