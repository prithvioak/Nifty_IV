from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='nifty_iv',
    version='0.1.0',
    description='plots for implied volatility on nifty',
    long_description=readme,
    author='Akshay Parhad, Prithvi Oak',
    author_email='',
    url='https://github.com/prithvioak/Nifty_IV',
    license=license,
    packages=find_packages()
    # packages=find_packages(exclude=('tests', 'docs'))
)