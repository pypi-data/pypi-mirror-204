from setuptools import setup, find_packages

setup(
    name="NeuralBaiscs",
    version="1.0.0",
    packages=find_packages(exclude=['test']),
    description='Neural network basics module. Number detection on images.',
    author='Henry Cook',
    author_email='henryscookolaizola@gmail.com',
    install_requires=['numpy', 'alive_progress', 'PIL', 'matplotlib', 'idx2numpy']
)