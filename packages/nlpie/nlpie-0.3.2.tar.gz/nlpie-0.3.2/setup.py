from setuptools import setup, find_packages

setup(
    name='nlpie',
    version='0.3.2',
    author='NLPie Research',
    author_email='info@nlpie.com',
    description='A lightweight clinical entity linking tool using distilled clinical language models from Huggingface and spaCy/ScispaCy',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nlpie-research/nlpie',
    packages=find_packages(include=["nlpie", "nlpie.*"]),
    install_requires=[
    'pandas==1.5.3',
    'scipy',
    'scispacy==0.5.1',
    'negspacy==1.0.3',
    'torch',
    'transformers==4.28.1'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
