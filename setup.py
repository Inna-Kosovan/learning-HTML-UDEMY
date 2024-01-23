from setuptools import setup, find_packages

setup(
    name="my_project",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # dependencies
    ],
    entry_points={
        'console_scripts': [
            'my_project=my_project.main:main',
        ],
    },
)
