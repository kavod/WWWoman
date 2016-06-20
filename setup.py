from setuptools import setup

setup(name='wwwoman',
      version='0.2',
      description='Extension of HTTPretty',
      url='https://github.com/kavod/WWWoman',
      author='Brice GRICHY',
      author_email='brice.grichy@gmail.com',
      license='GPL-3',
      packages=['wwwoman'],
      install_requires=[
          'httpretty',
          'requests'
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_requires=['nose'],
)
