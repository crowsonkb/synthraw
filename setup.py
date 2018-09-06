from pathlib import Path
import subprocess

from distutils.command.build import build
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def build_lib():
    command = ['cc', '-shared', '-fPIC', '-ltiff', 'synthraw/dng.c', '-o', 'synthraw/dng.so']
    print('Executing:', ' '.join(command))
    subprocess.check_call(command)


class CustomBuild(build):
    def run(self):
        build_lib()
        build.run(self)


class CustomDevelop(develop):
    def run(self):
        build_lib()
        develop.run(self)


class CustomInstall(install):
    def run(self):
        build_lib()
        install.run(self)


setup(name='synthraw',
      version='0.1',
      description='Synthesizes camera raw files.',
      long_description=(Path(__file__).resolve().parent / 'README.rst').read_text(),
      url='https://github.com/crowsonkb/synthraw',
      author='Katherine Crowson',
      author_email='crowsonkb@gmail.com',
      license='MIT',
      packages=['synthraw'],
      install_requires=['numpy>=1.14.3',
                        'pillow>=5.1.0'],
      package_data={
          'synthraw': ['dng.so'],
      },
      include_package_data=True,
      zip_safe=False,
      entry_points={
          'console_scripts': ['synthraw=synthraw.cli:main'],
      },
      cmdclass={
          'build': CustomBuild,
          'develop': CustomDevelop,
          'install': CustomInstall,
      })
