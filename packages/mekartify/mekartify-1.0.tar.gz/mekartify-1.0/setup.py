from setuptools import setup, find_packages

setup(
    name = "mekartify",
    version="1.0",
    description='Deskripsi singkat tentang package kamu',
    author='Nama pengarang',
    author_email='email@example.com',
    url='https://github.com/username/nama-package',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='keyword, keyword2',
    install_requires=[
        'pandas',
        'numpy',
    ],
)