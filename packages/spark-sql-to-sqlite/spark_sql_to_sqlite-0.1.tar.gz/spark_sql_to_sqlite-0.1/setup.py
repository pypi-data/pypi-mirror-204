from setuptools import setup, find_packages

setup(
    name='spark_sql_to_sqlite',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyspark',
        'pandas',
        'sqlite3',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
