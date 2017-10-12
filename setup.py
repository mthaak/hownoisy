from setuptools import setup, find_packages

setup(name='How Noisy',
      version='0.1',
      description='Automatic noise quantification in urban soundscapes',
      author='Martin ter Haak & Tianyu Zhou',
      author_email='',
      url='https://github.com/mthaak/how-noisy',
      download_url='http://github.com/mthaak/how-noisy/releases',
      packages=find_packages(),
      package_data={},
      include_package_data=True,
      long_description="TODO",
      keywords='audio sound soundscape environmental urban quantification',
      license='TODO',
      classifiers=[
          "TODO",
      ],
      install_requires=[
          'jams==0.2.2',
      ],
      extras_require={
          'docs': [],
          'tests': []
      }
      )
