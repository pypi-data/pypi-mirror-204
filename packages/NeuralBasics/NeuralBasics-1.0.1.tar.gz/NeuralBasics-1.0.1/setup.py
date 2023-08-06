from setuptools import setup, find_packages

setup(
    name="NeuralBaiscs",
    version="1.0.1",
    packages=find_packages(exclude=['test']),
    description='Neural network basics module. Number detection on images.',
    author='Henry Cook',
    author_email='henryscookolaizola@gmail.com',
    install_requires=['numpy', 'alive_progress', 'Pillow', 'matplotlib', 'idx2numpy']
)