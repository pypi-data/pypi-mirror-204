import setuptools
import codefast as cf

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythesyncer",
    version=cf.generate_version(),
    author="john",
    author_email="john@gmail.com",
    description="PythonTheSyncer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/private_repo/",
    packages=setuptools.find_packages(),
    package_data={
        setuptools.find_packages()[0]: [
            "bash/*"
        ]
    },
    install_requires=['codefast', 'fire', 'boto3'],
    entry_points={
        'console_scripts': ["pysyncer=pythesyncer.__init__:main"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
