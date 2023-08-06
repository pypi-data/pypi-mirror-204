from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='spark_sql_to_sqlite',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'pyspark',
        'pandas',
    ],
    classifiers=[
        # ... (other classifiers)
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",  # specify the format of the long description
)
