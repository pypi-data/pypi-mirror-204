from setuptools import setup,find_packages
version = '2.2'
setup(name='cellscanner',
      version='2.2',
      description='GREAT!!!!!!!!!!',
      author='zhw',
      author_email='1353595807@qq.com',
      packages=find_packages(),
      entry_points={
             'console_scripts': ['cellscanner = src.MainWindow:main']
        }
      )

