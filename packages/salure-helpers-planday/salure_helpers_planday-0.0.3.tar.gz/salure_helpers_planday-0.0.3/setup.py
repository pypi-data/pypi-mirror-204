from setuptools import setup


setup(
    name='salure_helpers_planday',
    version='0.0.3',
    description='Planday wrapper from Salure',
    long_description='Planday wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.planday"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=1',
        'pandas>=1,<=1.35',
        'requests>=2,<=3'
    ],
    zip_safe=False,
)