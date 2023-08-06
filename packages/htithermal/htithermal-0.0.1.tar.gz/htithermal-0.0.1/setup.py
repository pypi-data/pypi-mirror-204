from setuptools import find_packages, setup
import os

with open("app/Readme.md", "r") as f:
    long_description = f.read()

about = {}
with open("app/htithermal/src/_version.py") as f:
    exec(f.read(), about)
os.environ["PBR_VERSION"] = about["__version__"]

setup(
    name="htithermal",
    setup_requires=["pbr"],
    pbr=False,
    version=about["__version__"],
    # version="0.0.10",
    description="A package to plot AI/ML metrics at ease",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/somexgupta/htithermal",
    author="SomexGupta",
    author_email="gupta.somex@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=["pillow>= 7.0.0",                      
                      "numpy>= 1.19.2",
                      ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.7",
)
