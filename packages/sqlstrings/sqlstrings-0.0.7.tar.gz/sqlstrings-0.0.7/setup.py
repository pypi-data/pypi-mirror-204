from setuptools import setup

setup(
    name='sqlstrings',
    version='0.0.7',    
    description='Generates SQL query strings in multiple dialects.',
    keywords='sql strings generate query',
    url='https://github.com/alikellaway/sqlstrings',
    author='Ali Kellaway',
    author_email='ali.kellaway139@gmail.com',
    license='MIT',
    # package_dir={'':''},
    packages=['sqlstrings'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',         
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent'
    ]
)