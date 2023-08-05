from setuptools import setup, find_packages

setup(
    name='crowdcores-node',
    version='1.0.6',
    packages=find_packages(),
    install_requires=[
        'websockets',
        'torch',
        'transformers',

    ],
    entry_points={
        'console_scripts': [
            'crowdcores-node = crowdcores_node.manager:main',
            'crowdcores-node-runner = crowdcores_node.node:main',
        ]
    }
)
