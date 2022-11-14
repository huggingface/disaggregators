# Lint as: python3
""" HuggingFace/Disaggregators is an open library for disaggregating datasets.

Note:

   VERSION needs to be formatted following the MAJOR.MINOR.PATCH convention

Simple check list for release from AllenNLP repo: https://github.com/allenai/allennlp/blob/master/setup.py

To create the package for pypi.

0. Prerequisites:
   - Dependencies:
     - twine: "pip install twine"
   - Create an account in (and join the 'disaggregators' project):
     - PyPI: https://pypi.org/
     - Test PyPI: https://test.pypi.org/

1. Change the version in:
   - __init__.py
   - setup.py

2. Commit these changes: "git commit -m 'Release: VERSION'"

3. Add a tag in git to mark the release: "git tag VERSION -m 'Add tag VERSION for pypi'"
   Push the tag to remote: git push --tags origin main

4. Build both the sources and the wheel. Do not change anything in setup.py between
   creating the wheel and the source distribution (obviously).

   First, delete any "build" directory that may exist from previous builds.

   For the wheel, run: "python setup.py bdist_wheel" in the top level directory.
   (this will build a wheel for the python version you use to build it).

   For the sources, run: "python setup.py sdist"
   You should now have a /dist directory with both .whl and .tar.gz source versions.

5. Check that everything looks correct by uploading the package to the pypi test server:

   twine upload dist/* -r pypitest --repository-url=https://test.pypi.org/legacy/

   Check that you can install it in a virtualenv/notebook by running:
   pip install -i https://testpypi.python.org/pypi disaggregators

6. Upload the final version to actual pypi:
   twine upload dist/* -r pypi

7. Fill release notes in the tag in GitHub once everything is looking hunky-dory.

8. Change the version in __init__.py and setup.py to X.X.X+1.dev0 (e.g. VERSION=1.18.3 -> 1.18.4.dev0).
   Then push the change with a message 'set dev version'
"""

from setuptools import find_packages, setup


REQUIRED_PKGS = [
    # Utilities from PyPA to e.g., compare versions
    "packaging",
]

TESTS_REQUIRE = [
    # test dependencies
    "pytest",
    "pytest-datadir",
    "pytest-xdist",
]

QUALITY_REQUIRE = ["black~=22.0", "flake8>=3.8.3", "isort>=5.0.0", "pyyaml>=5.3.1"]


EXTRAS_REQUIRE = {
    "dev": TESTS_REQUIRE + QUALITY_REQUIRE,
    "tests": TESTS_REQUIRE,
    "quality": QUALITY_REQUIRE,
}

setup(
    name="disaggregators",
    version="0.1.1",  # expected format is one of x.y.z.dev0, or x.y.z.rc1 or x.y.z (no to dashes, yes to dots)
    description="HuggingFace community-driven open-source library for dataset disaggregation",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="HuggingFace Inc.",
    author_email="nima@huggingface.co",
    url="https://github.com/NimaBoscarino/disaggregators",
    download_url="https://github.com/NimaBoscarino/disaggregators/tags",
    license="Apache 2.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=REQUIRED_PKGS,
    extras_require=EXTRAS_REQUIRE,
    python_requires=">=3.7.0",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="machine learning evaluate evaluation disaggregation",
    zip_safe=False,  # Required for mypy to find the py.typed file
)
