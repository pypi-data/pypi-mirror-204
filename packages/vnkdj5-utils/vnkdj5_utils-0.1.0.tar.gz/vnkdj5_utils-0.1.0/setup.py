from setuptools import find_packages, setup
setup(
    name='vnkdj5_utils',
    packages=find_packages(include=["vnkdj5_utils"]),
    version='0.1.0',
    description='test package',
    author='vnkdj5',
    license='MIT',
    install_requires=["redis==4.5.4"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
