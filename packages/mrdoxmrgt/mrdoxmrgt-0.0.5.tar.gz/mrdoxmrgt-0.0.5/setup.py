from setuptools import setup, find_packages

setup(
    name='mrdoxmrgt',
    packages=find_packages(),
    include_package_data=True,
    version="0.0.5",
    description='A small example package',
    long_description="A small example package HI",
    long_description_content_type="text/markdown",
    author='MR_GT',
    author_email='friendyt89@gmail.com',
    url='https://github.com/GreyTechno/SMS_Forwarder',
    download_url="https://github.com/GreyTechno/gtf/archive/pypi.zip",
        keywords=['a1', 'a2', 'a3', 'a3', 'a4',
                  'a5', 'a6', 'a7', 'a8', 'a9'],
    classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
            'Environment :: Console',
    ],
    install_requires=["requests"],
    license='GPL',
    entry_points={
            'console_scripts': [
                'mrdoxmrgt = mrdoxmrgt._main_:main',
            ],
    },
    python_requires='>=3.5'
)
