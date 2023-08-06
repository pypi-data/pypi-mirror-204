import os
from glob import glob
from setuptools import setup, find_packages
import colemen_utilities.build_utils.general as _gen


VERSION='0.0.1'
DESCRIPTION = 'volent'
LONG_DESCRIPTION = 'None'


_root_path = f"{os.getcwd()}/volent"
PY_MODULES = _gen.list_py_modules(
    _root_path,
    additions=['main']
)
_gen.purge_dist()

DATA_FILES = [
    # ('Lib/site-packages/volent/documentation', glob('documentation/*.md')),
    # ('where the files will be installed', glob('where to get the files to include')),
]

# Setting up
setup(
    name="colemen_volent",
    version=VERSION,
    author="Colemen Mitchell Atwood",
    author_email="<atwoodcolemen@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    py_modules=PY_MODULES,
    # add any additional packages that
    # need to be installed along with your package. Eg: 'caer'
    install_requires=[
        'colemen_utils',
    ],

    keywords=['python'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
