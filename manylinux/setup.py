#!/usr/bin/env python
import sys
import os
from setuptools import setup, Extension
from setuptools.dist import Distribution

if not 'VERSION' in os.environ:
    raise Exception('Script usage: VERSION=x.x.x python3 setup.py sdist')
if not 'OPENVINO_LIBS_DIR' in os.environ:
    raise Exception('Specify OPENVINO_LIBS_DIR to OpenVINO binaries folder')
if not 'TBB_DIR' in os.environ:
    raise Exception('Specify TBB_DIR to TBBConfig.cmake folder')

libs_dir = os.environ['OPENVINO_LIBS_DIR']
py_version = '{}.{}'.format(sys.version_info[0], sys.version_info[1])


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True


def normalize_lib_name(name):
    if sys.platform == 'win32':
        return name + '.dll'
    elif sys.platform == 'linux':
        return 'lib' + name + '.so'
    else:
        raise Exception('Unknown platform: ' + sys.platform)

# Add shared libraries to package
data = [ libs_dir + '/' + normalize_lib_name(name) for name in [
    'inference_engine',
    'inference_engine_transformations',
    'ngraph',
    'inference_engine_onnx_reader',
    'inference_engine_preproc',
    'MKLDNNPlugin',
]]

data += [libs_dir + '/plugins.xml']

# Add TBB shared library
if sys.platform == 'win32':
    data += [os.environ['TBB_DIR'] + '/../bin/tbb.dll']
    data += [
        libs_dir + '/python_api/python{}/openvino/inference_engine/ie_api.pyd'.format(py_version),
        libs_dir + '/python_api/python{}/openvino/inference_engine/constants.pyd'.format(py_version),
    ]
    data = [('../../openvino/inference_engine', data)]
elif sys.platform == 'linux':
    data += [os.environ['TBB_DIR'] + '/../lib/libtbb.so']
    data = [('../../experimental_openvino_python.libs', data),
            ('../../openvino/inference_engine', [
                libs_dir + '/python_api/python{}/openvino/inference_engine/ie_api.so'.format(py_version),
                libs_dir + '/python_api/python{}/openvino/inference_engine/constants.so'.format(py_version),
            ])]
else:
    raise Exception('Unknown platform: ' + sys.platform)


setup(name='experimental-openvino-python',
      version=os.environ['VERSION'],
      author='Dmitry Kurtaev',
      url='https://github.com/dkurt/openvino-python-manylinux/',
      distclass=BinaryDistribution,
      packages=['openvino', 'openvino.inference_engine'],
      package_dir={'openvino': libs_dir + '/python_api/python{}/openvino'.format(py_version)},
      data_files=data,
      install_requires=['numpy'],
)
