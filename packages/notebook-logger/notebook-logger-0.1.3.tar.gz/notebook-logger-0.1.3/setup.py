import setuptools

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='notebook-logger',
    version='0.1.3',
    license='Apache-2.0',
    author='Daniel Lee',
    author_email='rootuser.kr@gmail.com',
    description='Simple logger for jupyter notebook user',
    long_description=long_description,
    url='https://github.com/asulikeit/notebook-logger',
    long_description_content_type='text/markdown',
    packages=['notebook_logger'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ]
)