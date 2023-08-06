from setuptools import setup, find_packages


setup(
    name='web3_auto',
    version='1.3.0',
    license='MIT',
    author="ZarKane",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/ZarKane111/web3_auto',
    keywords='web3 to_checksum checksum from_key private key from_mnemonic mnemonic',
    install_requires=[
          'requests', 'web3',
      ],

)