#!/usr/bin/env python

import sys
import os
from fnmatch import fnmatch
from setuptools import setup, find_packages
from setuptools.command.install import install

if not 'VERSION' in os.environ:
    raise Exception('Set VERSION environment variable')

# frameworks = []
# for name in os.listdir('model_optimizer'):
#     if fnmatch(name, 'mo_*.py'):
#         print(name)
# exit()
# print(find_packages())
# exit()

deps = [
    'networkx>=1.11',
    'defusedxml>=0.5.0',
    'numpy>=1.14.0',
]

with open('__init__.py', 'wt') as f:
    f.write('import sys; import os; sys.path.append(os.path.dirname(__file__))')

class InstallCmd(install):
    def run(self):
        install.run(self)
        print(self.install_purelib)
        # path = os.path.join(self.install_purelib, 'requirements_{}.txt'.format(framework))
        # with open(path, 'wt') as f:
        #     f.write('\n'.join(deps))

setup(name='experimental-openvino-python-mo',
        version=os.environ['VERSION'],
        author='Dmitry Kurtaev',
        url='https://github.com/dkurt/openvino-python-manylinux/',
        packages=find_packages(),
        # py_modules=['mo_{}'.format(framework)],
        # cmdclass={
        #     'install': InstallCmd,
        # },
        install_requires=deps,
        include_package_data=True,
)
