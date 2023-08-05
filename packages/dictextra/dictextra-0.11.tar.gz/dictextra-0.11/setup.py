from setuptools import setup, find_packages


setup(
    name='dictextra',
    version='0.11',
    license='MIT',
    author="Josiah Augustine Onyemaechi",
    author_email='josiah.augustine.o@gmail.com',
    packages=find_packages('./'),
    package_dir={'': './'},
    url='https://github.com/austitech/dictextra',
    keywords='python, dict, extension',
    install_requires=[],
)