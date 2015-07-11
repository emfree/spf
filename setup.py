from setuptools import setup

setup(
    name='spf',
    packages=['spf'],
    version='0.0.1',
    description='A Python stack-sampling profiler for distirbuted applications.',
    author='Eben Freeman',
    author_email='freemaneben@gmail.com',
    url='https://github.com/emfree/spf',
    include_package_data=True,
    install_requires=[
        'requests'
    ]
)
