import os
import sys
from shutil import rmtree

from setuptools import setup, find_packages, Command

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# Package meta-data.
NAME = 'openomics'
version='0.7.7'
DESCRIPTION = 'OpenOmics provides a bioinformatics API and web-app platform integrate and visualize the multiomics and clinical data.'
URL = 'https://github.com/JonnyTran/OpenOmics'
EMAIL = 'nhat.tran@mavs.uta.edu'
AUTHOR = 'Jonny Tran'

requirements = [
    'numpy', 'pandas', 'networkx>=2.1', 'dask', 'biopython', 'bioservices', 'h5py', 'dash'
]

setup_requirements = ['pytest-runner', 'twine']
test_requirements = ['pytest', ]

here = os.path.abspath(os.path.dirname(__file__))


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(version))
        os.system('git push --tags')

        sys.exit()


setup(
    name=NAME,
    version=version,
    packages=find_packages(include=['openomics']),
    package_dir={NAME: 'openomics',
                 'openomics_web': 'openomics_web'},
    url=URL,
    license='MIT license',
    install_requires=requirements,
    setup_requires=setup_requirements,
    extras_require={
            ':python_version == "2.7"': [
                'six==1.10',
                'lxml==4.3.5'
            ],
        },
    test_suite='tests',
    tests_require=test_requirements,
    classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            "Programming Language :: Python :: 2",
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ],
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=readme + '\n\n' + history,
# $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
    include_package_data=True,
    zip_safe=False,

)
