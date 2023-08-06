'''
Author: rui.li
Date: 2022-07-15 11:20:41
LastEditors: rui.li
LastEditTime: 2023-04-23 14:52:51
FilePath: /PythonCephStoreTool/setup.py
'''


from setuptools import setup, find_packages

setup(
    name="pyCeph",
    version="0.5.1",
    keywords=["pip", "pyCeph", "s3", "ceph"],
    description="ceph using tool",
    long_description="ceph using tool",
    license="MIT Licence",
    url="https://github.com/susufqx/pyCeph",
    author="susufqx",
    author_email="jiangsulirui@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "aioboto3",
        "boto3",
        "urllib3",
    ]
)
