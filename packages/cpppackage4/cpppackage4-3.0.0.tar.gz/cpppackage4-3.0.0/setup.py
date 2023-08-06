from setuptools import setup

setup(
    name='cpppackage4',
    version='3.0.0',
    description='A short description of my package',
    packages=['django_pdf_generator'],
    install_requires=[
        'requests>=2.25.1',
        'numpy>=1.19.5',
        'bdist_wheel'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    url='https://github.com/my_username/my_package',
    author='swapnil',
    author_email='swapnild333@gmail.com'
)
