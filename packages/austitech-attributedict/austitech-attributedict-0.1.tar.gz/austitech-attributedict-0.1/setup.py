from setuptools import setup, find_packages


setup(
    name='austitech-attributedict',
    version='0.1',
    license='MIT',
    author="Josiah Augustine Onyemaechi",
    author_email='josiah.augustine.o@gmail.com',
    packages=find_packages('./'),
    package_dir={'': './'},
    url='https://github.com/austitech/attributedict',
    keywords='python dict extension',
    install_requires=[],
)