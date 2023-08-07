#!/usr/bin python
# -*- coding: utf-8 -*-
'''
@Author: HornLive
@Time: 11 04, 2021
'''
from setuptools import find_packages
from setuptools import setup
import codecs
import os


def readme():
    with codecs.open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


version_file = 'python/version.py'


def get_version():
    if 'BUILD_EASYREC_DOC' in os.environ:
        os.system('bash -x scripts/build_read_the_docs.sh')
    with codecs.open(version_file, 'r') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']


def md_to_rst(from_file, to_file):
    """
    将markdown格式转换为rst格式
    @param from_file: {str} markdown文件的路径
    @param to_file: {str} rst文件的路径
    """
    import requests
    response = requests.post(
        url='http://c.docverter.com/convert',
        data={'to': 'rst', 'from': 'markdown'},
        files={'input_files[]': open(from_file, 'rb')}
    )

    if response.ok:
        with open(to_file, "wb") as f:
            f.write(response.content)


# md_to_rst("README.md", "README.rst")

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='silkynet',  # 包名称，也就是文件夹名称
    version=get_version(),
    description='machine learning kit for algorithm train platform',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='hornlee',
    author_email='hongen26@163.com',
    url='https://code.amh-group.com/model-platform/kflearn',
    license='MIT Licence',
    keywords='kflearn ymm',
    project_urls={
        'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/pypa/sampleproject/',
        'Tracker': 'https://github.com/pypa/sampleproject/issues',
    },
    platforms="any",
    # zip_safe=False,  # 此项需要，否则卸载报windows error错误
    # py_modules=["train"],  # 需要打包的文件夹下的py文件名词cal_similarity.py

    # find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),#排除一些包
    # packages = find_packages('src'),  # 包含所有src中的包
    # package_dir = {'':'src'},   # 告诉distutils包都在src下
    # packages=['kflearn', 'pkg'],
    packages=find_packages(),  # 需要打包的目录列表
    package_data={
        # 任何包中含有.txt文件，都包含它
        '': ['*.txt', '*.ini', '*.sh', '*.yaml', '*.json'],
        # 包含demo包data文件夹中的 *.dat文件
        # 'demo': ['data/*.dat'],
    },

    install_requires=['click', 'ruamel.yaml', 'numpy'],
    # 'numpy>=1.14', 'tensorflow>=1.7'
    python_requires='>=3',
    # entry_points={
    #     'console_scripts': [
    #         'kfl = kflearn.cmd.kfl_cmd:kfl',
    #         'foo = pkg:test',
    #         'bar = pkg.test:kfl',
    #     ],
    #     'gui_scripts': [
    #         'baz = pkg:test',
    #     ]
    # }
)
