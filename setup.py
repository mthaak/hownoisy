from setuptools import setup, find_packages

setup(
    name='HowNoisy',
    version='0.1',
    description='Automatic noise quantification in urban soundscapes',
    author='Martin ter Haak & Tianyu Zhou',
    author_email='',
    url='https://github.com/mthaak/how-noisy',
    download_url='http://github.com/mthaak/how-noisy/releases',
    packages=find_packages(),
    package_data={},
    include_package_data=True,
    long_description='',  # TODO
    keywords='soundscape urban quantification acoustic noise sound detection information retrieval',
    license='',  # TODO
    classifiers=[
    ],
    install_requires=[
        'librosa'
    ],
    extras_require={
        'docs': [],
        'tests': []
    },
    test_suite='tests',
)
