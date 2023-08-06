from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='newcode_utils',
    packages=['newcode_utils'],  # this must be the same as the name above
    version='0.1.2',
    description='Necessary elements for the development of apps.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Camilo Suarez',
    author_email='juancamilosuarezquinones@gmail.com',
    maintainer='NewCode_',
    maintainer_email='new.code.2523@gmail.com',
    url='https://github.com/New-Code-S-A-S/newcode_utils',  # use the URL to the github repo
    keywords=['utils', 'newcode-utils', 'NewCode', 'Audit'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
    setup_requires=['wheel'],
    include_package_data=True,
)
