from setuptools import setup, find_packages

setup(
    name='numering',
    version='0.9',
    license='MIT',
    author="sudo",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    long_description=open("README.md", "r").read(),
    long_description_content_type='text/markdown',
    keywords='numering',
    install_requires=[],
)