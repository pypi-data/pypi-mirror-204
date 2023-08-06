import os
import sys

from setuptools import setup, find_packages, Command
from shutil import rmtree
from har_to_case import __version__, __description__, __title__, __url__, __author__, __author_email__, __license__

file_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(file_path, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


class ParserCommand(Command):
    """Support setup.py upload."""
    ...

    def run(self):
        try:
            self.status('Removing previous builds ...')
            rmtree(os.path.join(file_path, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution ...')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine ...')
        os.system('twine upload dist/*')

        self.status('Pushing git tag ...')
        os.system('git tag v{0}'.format(__version__))
        os.system('git push --tags')

        sys.exit(0)


setup(
    name=__title__,
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='har json compare comparison case yaml yml',
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=['loguru~=0.6.0', 'haralyzer~=2.2.0', 'PyYAML~=6.0'],
    entry_points={
        'console_scripts': [
            'har2case = har_to_case.parse_har:main'
        ]
    },
    cmdclass={
        'har2case': ParserCommand
    }
)

# python setup.py sdist bdist_wheel
# python -m twine upload dist/*
