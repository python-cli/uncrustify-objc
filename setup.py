from setuptools import setup

setup(
    name='uncrustify-objc',
    version='1.0',
    py_modules=['uncrustify'],
    include_package_data=False,
    install_requires=[
        'click'
    ],
    entry_points='''
        [console_scripts]
        uncrustify-objc=uncrustify:cli
    ''',
)
