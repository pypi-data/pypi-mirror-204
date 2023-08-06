from setuptools import setup, find_packages

setup(
    name='nlpie',
    version='0.3',
    author='NLPie Research',
    author_email='info@nlpie.com',
    description='A lightweight clinical entity linking tool using distilled clinical language models from Huggingface and spaCy/ScispaCy',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nlpie-research/nlpie',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scipy',
        'scispacy',
        'negspacy',
        'torch',
        'transformers'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
