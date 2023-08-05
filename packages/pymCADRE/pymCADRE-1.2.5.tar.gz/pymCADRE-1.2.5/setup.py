from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pymCADRE',
    version='1.2.5',
    description='The pymCADRE tool is an advanced re-implementation of the metabolic Context-specificity Assessed by Deterministic Reaction Evaluation (mCADRE) algorithm in Python. It constructs tissue-specific metabolic models by leveraging gene expression data and literature-based evidence, along with network topology information.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/draeger-lab/pymCADRE',
    author='Nantia Leonidou',
    author_email='nantia.leonidou@uni-tuebingen.de',
    license=' GPL-3.0',
    keywords=['pymCADRE', 'systems biology', 'tissue-specific metabolic models'],
    #packages=find_packages(include=['pymCADRE_code']),
    #py_modules=['SBOannotator', 'main'],
    #packages=find_packages(),
    packages=['test_dataset','pre_processing_scripts',
        'pymCADRE.check','pymCADRE.prune','pymCADRE.rank'],
    include_package_data=True,
    install_requires=['pandas',
                      'numpy',
                      'cobra',
                      'requests']
)
