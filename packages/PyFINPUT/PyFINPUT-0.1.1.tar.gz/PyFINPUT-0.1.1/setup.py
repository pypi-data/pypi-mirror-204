from setuptools import setup, find_packages

setup(
    name='PyFINPUT',
    version='0.1.1',
    license='GNU General Public License v3.0',
    author="Benedict Saunders",
    author_email='benedictsaunders@gmail.com',
    packages=find_packages('src/PyFINPUT'),
    package_dir={'': 'src'},
    url='https://github.com/benedictsaunders/PyFINPUT',
    keywords='input, file, keywords',
    install_requires=[],
    description = "A simple parser for a file input, akin to the format of argparse",
    long_description="""# PyFINPUT!\n\n  ## A small package to use a file to input multiple arguments to a script.\n\n""",
    long_description_content_type='text/markdown',
)