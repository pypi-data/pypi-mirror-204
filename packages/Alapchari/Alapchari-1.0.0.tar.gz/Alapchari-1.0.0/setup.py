from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='Alapchari',
    version='1.0.0',
    author='Nur Mahmud Ul Alam Tasin',
    author_email='nmuatasin2005@gmail.com',
    description='Lets you interact with the Alapchari Chatbot.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    license="MIT License",
    platforms=["x86","x86_64","arm"],
    url="https://github.com/NurTasin/Alapchari-Python"
)
