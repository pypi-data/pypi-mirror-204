try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires: list[str] = [
    "setuptools",
    "tabulate",
]
"""All required (i.e., for functionality) dependencies that are installed when running `pip install SAPsim`.

Non-functional (e.g., formatting, documentation) dependencies listed in requirements.txt."""

setup(
    name="SAPsim",
    # Version number that appears on PyPI and Test PyPI
    version="0.0.1",
    description="Simulation of SAP (Simple As Possible) computer programs from COMP311 (Computer Organization) @ UNC",
    author="Jesse Wei",
    author_email="jesse@cs.unc.edu",
    url="https://github.com/jesse-wei/sapsim",
    download_url="https://github.com/jesse-wei/SAPsim/releases",
    keywords=[
        "SAP",
        "SAPsim",
        "UNC",
        "COMP311",
    ],
    install_requires=install_requires,
    tests_require=install_requires + ["tox", "pytest", "pytest-cov"],
    # See https://docs.python.org/3/distutils/setupscript.html#listing-whole-packages
    # or https://setuptools.pypa.io/en/latest/userguide/package_discovery.html
    # for what these mean
    package_dir={"": "src"},
    packages=["SAPsim", "utils"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
