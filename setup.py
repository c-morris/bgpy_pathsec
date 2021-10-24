from setuptools import setup, find_packages
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# https://stackoverflow.com/a/58534041/8903959
setup(
    name='bgp_simulator_policies',
    author="Cameron Morris",
    author_email="cameron.morris@uconn.edu",
    version="0.0.1",
    url='',
    license="BSD",
    description="Policies and Attacks for jfuruness' BGP simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["Furuness", "BGP", "Simulations", "ROV"],
    include_package_data=True,
    python_requires=">=3.7",
    packages=find_packages(),
    install_requires=[
        'lib_bgp_simulator',
        'lib_caida_collector',
        'lib_utils',
        'tikzplotlib',
        'pytest',
        'tqdm',
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'],
    entry_points={
        #'console_scripts': 'lib_bgp_simulator = lib_bgp_simulator.__main__:main'
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
