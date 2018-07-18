from setuptools import setup
import os
import shutil

here = os.path.abspath(os.path.dirname(__file__))
default_root_path = os.path.expanduser('~/.uncrustify')

if not os.path.exists(default_root_path):
    os.mkdir(default_root_path)


cfg_file_name = 'uncrustify.cfg'
cfg_file_path = os.path.join(default_root_path, cfg_file_name)

if not os.path.exists(cfg_file_path):
    shutil.copyfile(os.path.join(here, cfg_file_name), cfg_file_path)
    print("Created %s" % cfg_file_path)


ignore_file_name = 'uncrustify_ignore_global'
ignore_file_path = os.path.join(default_root_path, ignore_file_name)

if not os.path.exists(ignore_file_path):
    shutil.copyfile(os.path.join(here, ignore_file_name), ignore_file_path)
    print("Created %s" % ignore_file_path)


def readme():
    with open('README.txt') as f:
        return f.read()

setup(
    name='uncrustify-objc',
    version='1.3',
    author='Will Han',
    author_email='xingheng.hax@qq.com',
    license='MIT',
    keywords='uncrustify objective-c objc code beauty format',
    url='https://github.com/xingheng/uncrustify-objc',
    description='Use uncrustify to format the objective-c files under the specified project path',
    long_description=readme(),
    py_modules=['uncrustify_objc'],
    include_package_data=True,
    install_requires=[
        'click',
        'pathspec'
    ],
    entry_points='''
        [console_scripts]
        uncrustify-objc=uncrustify_objc:cli
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Objective C',
        'Programming Language :: Unix Shell',
        'Topic :: Software Development :: Version Control',
        'Topic :: System :: Shells',
        'Topic :: Terminals',
        'Topic :: Text Processing :: Linguistic',
      ],
)
