from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="we_factor_quad",
    version="0.0.3",
    author="Xia Zeyu",
    author_email="xiazeyu@wealthengine.cn",
    description="Factor Quad, a data structure for factor analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://192.168.1.7:10600/xiazeyu/we_factor_quad.git",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.yml'],
        'ret_data': ["*.xlsx"],
    },
    install_requires=[
        'numpy',
        'pandas',
        'arrow',
        'sqlalchemy',
        'scikit-learn',
        'scipy',
        'statsmodels',
        'six',
        'sshtunnel',
        'openpyxl',
        'we_dms',
        'numba',
        "wiserdata",
        "pymysql"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    zip_safe=True,
)
