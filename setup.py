from setuptools import find_packages, setup

setup(
    name='utils',
    packages=find_packages(include=['utils']),
    version='0.1.0',
    description='Several utility functions I use in all my (deep-learning) projects.',
    author='Nikos Tsiknakis',
    license='MIT',
    install_requires=["PyYAML", "dotmap", "natsort", "numpy", "torch", "tqdm", "psutil"],
)
