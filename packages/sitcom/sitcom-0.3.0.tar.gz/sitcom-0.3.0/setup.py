from setuptools import setup

setup(
    name='sitcom',
    version='0.3.0',
    packages=['sitcom'],
    url='https://github.com/pu3/SITCoM',
    license='MIT',
    author='Purvi Udhwani',
    author_email='purviaries@aries.res.in',
    description='SITCoM: SiRGraF Integrated Tool for Coronal dynaMics',
    install_requires=[
        'PyQt5','opencv-python','numpy'
    ],
    package_data={
        'sitcom': ['load/*','font/*','icon/*','data/*']
    }
)
