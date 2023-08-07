from setuptools import setup, find_packages

classifiers= [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3' 
]

setup(

    name='discounts',
    version='0.0.8',
    description='Package created for using discount function',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Akash Sane',
    author_email='x21220956@student.ncirl.ie',
    license='MIT',
    classifiers=classifiers,
    keywords='discount',
    packages=find_packages(),
    install_requires=['']
)