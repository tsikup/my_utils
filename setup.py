from setuptools import find_packages, setup

setup(
    name='utils',
    version='0.1.0',
    packages=find_packages(include=['utils']),
    url='https://github.com/tsikup/he_preprocessing',
    license='MIT',
    author='Nikos Tsiknakis',
    author_email='tsiknakisn@gmail.com',
    description='Several utility functions I use in all my (deep-learning) projects.',
    install_requires=["PyYAML", "dotmap", "natsort", "numpy", "torch", "tqdm", "psutil"],
)
