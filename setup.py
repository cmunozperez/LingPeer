from setuptools import setup, find_packages

setup(
    name='LingPeer',
    version='0.1',
    description='An app that retrieves from Lingbuzz potential reviewers for papers in theoretical linguistics.',
    author='Carlos Muñoz Pérez',
    author_email='cmunozperez@filo.uba.ar',
    packages=find_packages(),
    install_requires=[
        'joblib==1.2.0',
        'spacy==3.6.1',
        'pandas==1.4.2',
        'scikit-learn==1.3.1',
        'streamlit==1.26.0',
    ],
)