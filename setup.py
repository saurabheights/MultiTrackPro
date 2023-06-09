#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "linetimer>=0.1.5",
    "numpy>=1.24.3",
    "opencv-python>= 4.7.0",
    "pyqt6>=6.5.1",
]

test_requirements = [ ]

setup(
    author="Saurabh Khanduja",
    author_email='pixelperceive@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
    description="A multi-camera multi-object tracking library with its own labelling tool to annotate datasets.",
    entry_points = {
        'console_scripts': ['auto-annotate-pro=auto_annotate_pro:main'],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='multitrackpro, annotation, labelling, machine-learning, deep-learning, vision, ML, DL, AI, YOLO',
    name='multitrackpro',
    packages=find_packages(include=['multitrackpro', 'multitrackpro.*']),
    python_requires='>=3.6',
    scripts=['multitracker/auto_annotate_pro.py'],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/saurabheights/multitrackpro',
    version='0.1.1',
    zip_safe=False,
)
