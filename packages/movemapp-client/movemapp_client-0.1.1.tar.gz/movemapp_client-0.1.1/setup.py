from setuptools import setup, find_packages

setup(
    name="movemapp_client",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
         "carto",
         "python-dotenv"
    ],
    # dev dependencies
    extras_require={
        "dev": [
            "pytest",
            "python-dotenv"
            "autopep8",
        ]
    },
    description="A Python package for Movemapp client",
    author="Shoaib Burq",
    author_email="shoaib@geografia.com.au",
    url="https://github.com/geografia-au/movemapp_client",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
)
