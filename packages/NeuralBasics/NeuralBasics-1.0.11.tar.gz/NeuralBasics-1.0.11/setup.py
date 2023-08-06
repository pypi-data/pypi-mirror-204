from setuptools import setup, find_packages

setup(
    name="NeuralBasics",
    version="1.0.11",
    package_dir={"": "src"},
    packages=find_packages(include=['NeuralBasics', 'NeuralBasics.*'], where='src'),
    description='Neural network basics module. Number detection on images.',
    author='Henry Cook',
    author_email='henryscookolaizola@gmail.com',
    install_requires=['numpy', 'alive_progress', 'Pillow', 'matplotlib', 'idx2numpy']
)