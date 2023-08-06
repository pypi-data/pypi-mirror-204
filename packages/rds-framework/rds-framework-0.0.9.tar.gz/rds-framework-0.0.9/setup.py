import os
from setuptools import setup


def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders


def package_data_dirs(root, data_dirs):
    data_dirs_path = [x + '/*' for x in data_dirs]
    for data_dir in data_dirs:
        data_dirs_path += [x.replace(f'{root}/', '') + '/*' for x in fast_scandir(f'{root}/{data_dir}')]

    return {root: data_dirs_path}


requirements = [
    # config
    'dynaconf==3.1.11',

    # HTTP clients
    'requests==2.28.1',

    # LAIS public Python libraries
    'dbc-reader>=0.1.1',

    # Search engine
    'opensearch_py==2.0.0',
    'opensearch_dsl==2.0.1',
    'elasticsearch==7.17.6',
    'elasticsearch_dsl==7.4.0',
]

with open("requirements.txt", "w") as file1:
    for requirement in requirements:
        file1.write(f"{requirement}\n")
    file1.write("\n# DEV\n")
    file1.write("mypy\n")
    file1.write("lxml\n")
    file1.write("flake8\n")
    file1.write("types-requests\n")
    file1.write("pytest>=7.1.3\n")
    file1.write("pytest-cov>=4.0.0\n")
    file1.write("pytest-profiling>=1.7.0\n")
    file1.write("pdoc3\n")

setup(
    name='rds-framework',
    version='0.0.9',
    description='Framework para serviços do Rede de Dados em Saúde do LAIS',
    author='Kelson da Costa Medeiros',
    author_email='kelson.medeiros@lais.huol.ufrn.br',
    keywords=['rds', 'framework', 'cache', 'config', 'helper', 'searchengine'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    python_requires='>=3.7',
    install_requires=requirements,
    packages=[
        'rds_framework',
        'rds_framework.cache',
        'rds_framework.config',
        'rds_framework.helpers',
        'rds_framework.searchengine',
    ],
    package_dir={'rds_framework': 'rds_framework'},
    package_data=package_data_dirs('rds_framework', [])
)
