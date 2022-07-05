from setuptools import setup

setup(
    name='mjauto',
    version='0.1',
    description='Random prompts for Midjourney',
    author='Jordan Weaver',
    license='MIT',
    zip_safe=False,
    entry_points={
        'console_scripts': ['mjauto=mjauto.cli:main'],
    },
)
