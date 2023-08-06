from setuptools import setup

setup(
    name='osrs-lib',
    version='0.1.2',
    description='An OSRS library',
    url='https://github.com/shumatepf/osrs-lib',
    author='shumatepf',
    author_email='shumatepfs@gmail.com',
    license='Apache 2.0',
    packages=['osrs_lib'],
    install_requires=['bs4',
                      'asyncio',
                      'aiohttp',
                      ],
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.11',
    ],
)
