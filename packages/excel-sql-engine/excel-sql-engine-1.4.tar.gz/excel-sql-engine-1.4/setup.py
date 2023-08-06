import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="excel-sql-engine",
    version="V1.4",
    author="Fabien BATTINI",
    author_email="fabien.battini@gmail.com",
    description="A tiny SQL engine for Excel files, based on Openpyxl",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/fabien.battini/pyxlsql",
    keywords='excel sql',
    packages=setuptools.find_packages(),
    classifiers=[
        # see https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Office Suites",
    ],
    python_requires='>=3.6',
)