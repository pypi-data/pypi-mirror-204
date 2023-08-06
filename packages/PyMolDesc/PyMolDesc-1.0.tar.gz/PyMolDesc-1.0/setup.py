from setuptools import setup, find_packages


setup(
    name='PyMolDesc',
    version='1.0',
    license='MIT',
    author="Kamil Pytlak",
    author_email='kam.pytlak@gmail.com',
    packages=find_packages('PyMolDesc'),
    package_dir={'': 'PyMolDesc'},
    url='https://github.com/kamilpytlak/PyMolDesc',
    keywords='',
    install_requires=[
          'pandas', 'rdkit'
      ],

)