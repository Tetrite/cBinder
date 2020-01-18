from setuptools import setup, find_packages

setup(
    name="cBinder",
    version="1.0",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),

    install_requires=[
        "cffi==1.13.0",
        "robotpy-cppheaderparser==3.1.2",
        "wheel==0.33.6",
        "setuptools==41.6.0",
    ],
    extras_require={
        "dev": [
            "pytest==5.3.1",
        ]
    },
    package_data={'cBinder': ['setup.config']},

    # metadata to display on PyPI
    author="Tetrite",
    author_email="tetrite19@gmail.com",
    description="Generates python wrapper for calling libraries in C",
    keywords="cbinder so dll wrapper shared",
    url="https://github.com/Tetrite/cBinder",
)
