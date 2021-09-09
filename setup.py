from setuptools import find_packages
from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='hybridrd',
    version='0.1',
    description='Package intended to project and design hybrid rocket motors.',
    long_description=read('README.md'),
    author='Lucas Germano Rischioni',
    author_email='lucasgrischioni@gmail.com',
    url='https://github.com/lrischioni/hybrid-rocket-design',
    license_files='LICENSE.txt',
    license='GNU General Public License v3.0',
    platforms=['Linux', 'Windows'],
    packages=find_packages('src'),
    packages_dir={'', 'src'},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Researchers and students',
        'License :: GNU General Public License v3.0',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.85',
    ],
    install_requires=[
        'numpy>=1.19.2',
        'pandas>=1.1.3',
        'Jinja2>=2.11.2',
        'pyqtgraph>=0.11.0',
        'PyQt5>=5.15.4',
        'wine-ctl>=2.1;platform_system=="Linux"',
    ],
    entry_points={
        'console_scripts': [
            'hybridrd = hybridrd.__main__:main',
        ]
    },
)
