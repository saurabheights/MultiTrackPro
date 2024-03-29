#!/usr/bin/env python
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "ultralytics>=8.0.125",  # For object detection
    "linetimer>=0.1.5",
    "opencv-python>=4.7.0",
    "pyqt6>=6.5.1",
]

test_requirements = [ ]

setup(
    # Often evolving fields first
    name='multitrackpro',
    version='0.1.3',
    description="A multi-camera multi-object tracking software with its own labelling tool to annotate datasets.",
    # Almost static fields below
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
    entry_points = {
        'console_scripts': ['auto-annotate-pro=auto_annotate_pro:main'],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='multitrackpro, annotation, labelling, machine-learning, deep-learning, vision, ML, DL, AI, YOLO',
    packages=find_packages(include=['multitracker', 'multitracker.*']),
    python_requires='>=3.6',
    scripts=['multitracker/auto_annotate_pro.py'],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/saurabheights/multitrackpro',
    zip_safe=False,
)
