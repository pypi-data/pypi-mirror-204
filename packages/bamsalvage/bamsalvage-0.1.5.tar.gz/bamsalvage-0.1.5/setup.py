from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="bamsalvage",
    version="0.1.2",
    license="MIT",
    description="seq",
    author="Takaho A. Endo",
    url="github",
    packages=find_packages("src/bamsalvage"),
    package_dir={"": "src/bamsalvage"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/bamsalvage/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file('requirements.txt'),
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    entry_ponts={
        'console_scripts': ['bamsalvage=bamsalvage:start'],
    }
    
)