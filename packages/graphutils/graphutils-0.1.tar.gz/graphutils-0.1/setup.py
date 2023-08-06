from setuptools import setup, find_packages

setup(
    name='graphutils',
    version='0.1',
    author='Peng Ding',
    author_email='pding.dp@foxmail.com',
    description='utility codebase for graph-related projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Oaklight/graphutils',
    packages=find_packages(),
    install_requires=[
        'networkx',
        'pgmpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        "Operating System :: OS Independent",
    ],
)