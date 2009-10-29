from distutils.core import setup

long_description = open('README.rst').read()

setup(
    name='django-popular',
    version="0.0.2",
    package_dir={'popular': 'popular'},
    packages=['popular'],
    description='Experimental Django library for finding popular objects based on google analytics views',
    author='James Turk',
    author_email='jturk@sunlightfoundation.com',
    license='BSD License',
    url='http://github.com/sunlightlabs/django-popular/',
    long_description=long_description,
    platforms=["any"],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
    ],
)
