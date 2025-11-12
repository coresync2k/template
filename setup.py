from setuptools import setup, find_packages

setup(
    name='aa-fleetpings-templates',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=3.2',
        'allianceauth>=2.0',
    ],
    description='Template-System für aa-fleetpings',
    author='Your Name',
    python_requires='>=3.8',
)
