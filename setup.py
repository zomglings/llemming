from setuptools import find_packages, setup

long_description = ""
with open("README.md") as ifp:
    long_description = ifp.read()

with open("llemming/version.txt") as ifp:
    VERSION = ifp.read().strip()

setup(
    name="llemming",
    version=VERSION,
    packages=find_packages(),
    install_requires=[],
    extras_require={
        "dev": ["black"],
        "distribute": ["setuptools", "twine", "wheel"],
    },
    description="llemming: Just llm stuff",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Moonstream",
    author_email="nkashy1@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
    url="https://github.com/zomglings/llemming",
    entry_points={
        "console_scripts": [
            "llemming=llemming.cli:main",
        ]
    },
    package_data={
        "llemming": [
            "version.txt",
        ]
    },
    include_package_data=True,
)
