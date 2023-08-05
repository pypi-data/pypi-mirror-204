# adapted from https://github.com/deepmind/chex/blob/master/setup.py

import os

from setuptools import find_namespace_packages, setup

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def _get_version():
    with open(os.path.join(_CURRENT_DIR, "serket", "__init__.py")) as fp:
        for line in fp:
            if line.startswith("__version__") and "=" in line:
                version = line[line.find("=") + 1 :].strip(" '\"\n")
                if version:
                    return version
        raise ValueError("`__version__` not defined in `serket/__init__.py`")


def _parse_requirements(path):
    with open(os.path.join(_CURRENT_DIR, path)) as f:
        return [
            line.rstrip() for line in f if not (line.isspace() or line.startswith("#"))
        ]


setup(
    name="serket",
    version=_get_version(),
    url="https://github.com/ASEM000/serket",
    license="MIT",
    author="Mahmoud Asem",
    description=("JAX NN library."),
    long_description=open(os.path.join(_CURRENT_DIR, "README.md")).read(),
    long_description_content_type="text/markdown",
    author_email="asem00@kaist.ac.kr",
    keywords="python machine-learning pytorch jax",
    packages=find_namespace_packages(exclude=['examples", "tests","experimental']),
    install_requires=["jax>=0.4.0", "pytreeclass>=0.3.0", "kernex"],
    zip_safe=False,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
