#!/usr/bin/env python

"""The setup script."""
import time
from setuptools import setup, find_packages
# from llm4gpt import __version__

version = time.strftime("%Y.%m.%d.%H.%M.%S", time.localtime())

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().split('\n')

setup(
    author="LLM4GPT",
    author_email='313303303@qq.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Create a Python package.",
    entry_points={
        'console_scripts': [
            'llm4gpt=llm4gpt.clis.cli:cli'
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='llm4gpt',
    name='llm4gpt',
    packages=find_packages(include=['llm', 'llm.*']),

    test_suite='tests',
    url='https://github.com/yuanjie-ai/llm4gpt',
    version=version, # '0.0.0',
    zip_safe=False,
)

