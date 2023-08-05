from setuptools import setup, find_packages

setup(
    name='rian-alba-tools',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'nilearn',
        'numpy',
        'openpyxl',
        'pandas',
        'pingouin',
        'plotly',
        'progressbar',
        'ptitprince',
        'scipy',
        'seaborn',
        'sklearn',
        'statsmodels',
        'zentables',
        'joblib',
    ],
    url='https://github.com/RianBogley/rian-alba-tools/',
    author='Rian Bogley',
    author_email='rianbogley@gmail.com',
    description='',
)
