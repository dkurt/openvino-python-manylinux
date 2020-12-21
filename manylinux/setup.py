#!/usr/bin/env python
import sys
import os
from setuptools import setup, Extension

if not 'VERSION' in os.environ:
    raise Exception('Script usage: VERSION=x.x.x python3 setup.py sdist')
if not 'OPENVINO_LIBS_DIR' in os.environ:
    raise Exception('Speify OPENVINO_LIBS_DIR to OpenVINO binaries folder')

libs_dir = os.environ['OPENVINO_LIBS_DIR']

py_version = '{}.{}'.format(sys.version_info[0], sys.version_info[1])

extension_module = Extension(
    'experimental-openvino-python.extension',
    sources=[],
    library_dirs=[libs_dir],
    libraries=['inference_engine'],
)

setup(name='experimental-openvino-python',
      version=os.environ['VERSION'],
      author='Dmitry Kurtaev',
      url='https://github.com/dkurt/openvino-python-manylinux/',
      ext_modules=[extension_module],
      packages=['openvino', 'openvino.inference_engine'],
      package_dir={'openvino': libs_dir + '/python_api/python{}/openvino'.format(py_version)},
      package_data={
          'openvino': [
              # libs_dir + '/python_api/python{}/openvino/inference_engine/ie_api.so'.format(py_version),
              # libs_dir + '/python_api/python{}/openvino/inference_engine/constants.so'.format(py_version),
          ],
      },
      data_files=[('../../experimental_openvino_python.libs', [
        libs_dir + '/plugins.xml',
        # libs_dir + '/libinference_engine_ir_reader.so',
        # libs_dir + '/libinference_engine_onnx_reader.so',
        # libs_dir + '/libinference_engine_preproc.so',
        # libs_dir + '/libMKLDNNPlugin.so',
        # '/openvino/bin/intel64/Release/lib/libHeteroPlugin.so',
        # '/openvino/bin/intel64/Release/lib/libclDNNPlugin.so',
        # '/openvino/bin/intel64/Release/lib/libGNAPlugin.so',
        # '/openvino/bin/intel64/Release/lib/libMultiDevicePlugin.so',
      ])],
      install_requires=['numpy'],
)
