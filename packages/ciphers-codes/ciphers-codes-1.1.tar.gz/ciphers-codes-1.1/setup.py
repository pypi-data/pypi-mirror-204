from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ciphers-codes',
    version='1.1',
    description="""A package that provides various encryption and decryption ciphers.

    The package includes the following ciphers:
    - Caesar Cipher
    - Vigenere Cipher
    - Playfair Cipher
    - Rail Fence Cipher
    - Columnar Transposition Cipher

    Documentation:
    https://github.com/yourusername/ciphers_codes
    """,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ciphers_codes",
    author='Your Name',
    author_email='your-email@example.com',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
