from setuptools import setup, find_packages

setup(
    name='lovehim',
    version='0.51',
    packages=find_packages(),
    install_requires=[
        'openai',
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'lovehim = lovehim.get_verse:main',
        ],
    },
)
