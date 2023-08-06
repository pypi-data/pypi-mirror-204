import setuptools

setuptools.setup(
    name="myscapyhelper",
    version="0.3.2",
    author="Sdst",
    author_email="",
    description="A collection of utilities for network analysis",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'scapy',
        'netifaces'
    ]
)