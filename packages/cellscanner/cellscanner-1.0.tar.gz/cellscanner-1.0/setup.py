from setuptools import setup,find_packages
version = '1.0'
setup(name='cellscanner',
      version='1.0',
      description='GREAT!!!!!!!!!!',
      author='zhw',
      author_email='1353595807@qq.com',
      packages=find_packages(),
      entry_points={
             'console_scripts': ['cellscanner = code.MainWindow:main']
        }
      )

