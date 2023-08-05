from setuptools import setup, find_packages

VERSION = '0.1.2'
DESCRIPTION = 'Demo for convex clustering'
LONG_DESCRIPTION = 'Showing convex clustering (with uniform weight) only produces circular clusters'

setup(
    name="ccDemo",
    version=VERSION,
    description=DESCRIPTION,
    url="https://github.com/canhhao/convexclustering",
    long_description=LONG_DESCRIPTION,
    author="Canh Hao Nguyen",
    author_email="canhhao@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=[         
        'pandas',         
        'numpy',
        'matplotlib',
        'sklearn',
    ],
    keywords='convex clustering',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)