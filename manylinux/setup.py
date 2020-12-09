#!/usr/bin/env python
import sys
import os
from setuptools import setup, Extension

if not 'VERSION' in os.environ:
    raise Exception('Script usage: VERSION=x.x.x python3 setup.py sdist')

py_version = '{}.{}'.format(sys.version_info[0], sys.version_info[1])

extension_module = Extension(
        'experimental-openvino-python.extension',
        sources=[],
        library_dirs=['/openvino/bin/intel64/Release/lib/'],
        libraries=['inference_engine'],
)

setup(name='experimental-openvino-python',
      version=os.environ['VERSION'],
      author='Dmitry Kurtaev',
      url='https://github.com/dkurt/openvino-python-manylinux/',
      ext_modules=[extension_module],
      packages=['openvino', 'openvino.inference_engine'],
      package_dir={'openvino': '/openvino/bin/intel64/Release/lib/python_api/python{}/openvino'.format(py_version)},
      package_data={
          'openvino': [
              '/openvino/bin/intel64/Release/lib/python_api/python{}/openvino/inference_engine/ie_api.so'.format(py_version),
              '/openvino/bin/intel64/Release/lib/python_api/python{}/openvino/inference_engine/constants.so'.format(py_version),
          ]
      },
)
