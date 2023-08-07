import setuptools
from setuptools import find_packages


# VERSION = '0.0.1'
PACKAGE_NAME = 'aireplication'
AUTHOR = 'Andrew'
AUTHOR_EMAIL = "andrewlee1807@gmail.com"
URL = 'https://github.com/andrewlee1807/ai-replicate'

LICENSE = 'Apache-2.0 license'
DESCRIPTION = "Private API for Andrew"
from pathlib import Path
this_file = Path(__file__).resolve()
readme_path = this_file.parent / "README.md"
readme_content = readme_path.read_text(encoding="utf-8")

LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    'scikit-learn',
    'pandas',
    'tensorflow',
    'tensorflow_addons',
    'pyyaml'
]
KEYWORDS = ['python', 'blackhole', 'aireplication']

setuptools.setup(
    name=PACKAGE_NAME,
    # version=VERSION,
    package_data={"": ["README.md"]},
    packages=find_packages(exclude=("*test*",)),
    url=URL,
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=readme_content,
    install_requires=INSTALL_REQUIRES,
    keywords=KEYWORDS,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
