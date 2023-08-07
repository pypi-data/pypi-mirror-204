from setuptools import setup, find_packages
# pylint: disable = relative-import
import obsutils

pkgs = find_packages()

if __name__ == '__main__':
    name = 'obsutils'

    requirements = ['esdk-obs-python']

    setup(
        name=name,
        version='1.0.7',
        description='hw modelarts obs utils',
        # long_description='',
        # author='Taichu platform team',
        # author_email='noreply@noreply.com',
        python_requires=">=3.6.0",
        url='',
        # keywords='Serving Deep Learning Inference AI',
        packages=pkgs,
        install_requires=requirements,
        include_package_data=True,
        # license='Apache License Version 2.0'
    )
