from setuptools import setup


def readme():
    with open('README.md', 'r') as f:
        return f.read()


version = {}
with open('parse_NMR_dataset/_version.py', 'r') as fp:
    exec(fp.read(), version)


setup(
    name='parse NMR dataset',
    version=version['__version__'],
    description='A Python3 module to parse experimental information from a Bruker NMR dataset.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: ',
      ],
    keywords='NMR, Bruker, Structural biology ',
    url='http://github.com/normcyr/parse_NMR_dataset',
    author='Normand Cyr',
    author_email='normand.cyr@umontreal.ca',
    license='GNU GPLv3',
    packages=['parse_NMR_dataset'],
    entry_points={
        'console_scripts': ['parse_data=parse_NMR_dataset.parse_dataset:main'],
    },
    install_requires=[
        'nmrglue==0.7',
        'json2html==1.3.0',
        ],
    zip_safe=False,
    include_package_data=True,
    python_requires='>=3.5',
)
