from setuptools import setup

setup(
    name='pynyol',
    version='0.1.3',
    author='Juanma López',
    author_email='lopezjuanma96@gmail.com',
    packages=['pynyol', 'pynyol.test'],
    package_dir={'': '.'},
    scripts=['bin/express_a_num.py'],
    url='https://pypi.org/project/pynyol',
    license='LICENSE.txt',
    description='Package aimed at helping with processing the spanish language.',
    long_description=open('README.txt').read(),
    install_requires=[
    ],
)