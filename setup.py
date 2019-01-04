import sys

from setuptools import setup

options = dict(
    name='booker',
    version='1.0.0',
    license='MIT',
    author='nvms',
    author_email='jon@pye.rs',
    packages=['booker'],
    url='https://github.com/nvms/booker',
    keywords=[
        'schedule', 'scheduling', 'scheduler',
        'cron', 'job' 'cron job', 'task',
        'cron task', 'task scheduler', 'task scheduling'
    ],
    classifiers=[
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)

setup(**options)
