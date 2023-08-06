import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dorsa_logging',                           # should match the package folder
    packages=['dorsa_logging'],                     # should match the package folder
    version='1.1.0',                                # important for updates
    license='Apache License 2.0',                                  # should match your chosen license
    description='Log application happenings',
    long_description=long_description,              # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Dorsa-co',
    author_email='info@dorsa-co.ir',
    url='https://github.com/DORSA-co/modules/tree/main/Dorsa_Logging', 
    project_urls = {                                # Optional
        "Bug Tracker": "https://github.com/DORSA-co/modules/tree/main/Dorsa_Logging/issues"
    },
    install_requires=['dorsa_datetime'],                  # list all packages that your package uses
    keywords=["pypi", "dorsa_logging"], # descriptive meta-data
    classifiers=[                                   # https://pypi.org/classifiers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
