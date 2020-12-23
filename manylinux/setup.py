#!/usr/bin/env python
import sys
import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.file_util import copy_file
from distutils.sysconfig import get_config_var

if not 'VERSION' in os.environ:
    raise Exception('Script usage: VERSION=x.x.x python3 setup.py sdist')
if not 'OPENVINO_LIBS_DIR' in os.environ:
    raise Exception('Specify OPENVINO_LIBS_DIR to OpenVINO binaries folder')
if not 'TBB_DIR' in os.environ:
    raise Exception('Specify TBB_DIR to TBBConfig.cmake folder')

libs_dir = os.environ['OPENVINO_LIBS_DIR']
py_version = '{}.{}'.format(sys.version_info[0], sys.version_info[1])

if sys.platform == 'win32':
    ext = '.pyd'
elif sys.platform == 'linux':
    ext = '.so'
else:
    raise Exception('Unknown platform: ' + sys.platform)

extensions = [
    Extension(
        'openvino.inference_engine.ie_api',
        sources=[libs_dir + '/python_api/python{}/openvino/inference_engine/ie_api{}'.format(py_version, ext)],
    ),
    Extension(
        'openvino.inference_engine.constants',
        sources=[libs_dir + '/python_api/python{}/openvino/inference_engine/constants{}'.format(py_version, ext)],
    )
]

# source: https://github.com/openvinotoolkit/openvino/pull/3582
class copy_ext(build_ext):
    def run(self):
        for extension in self.extensions:
            src = extension.sources[0]
            dst = self.get_ext_fullpath(extension.name)
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
            copy_file(src, dst, verbose=self.verbose, dry_run=self.dry_run)


def normalize_lib_name(name):
    if sys.platform == 'win32':
        return name + '.dll'
    elif sys.platform == 'linux':
        return 'lib' + name + '.so'
    else:
        raise Exception('Unknown platform: ' + sys.platform)

# Add shared libraries to package
data = [ libs_dir + '/' + normalize_lib_name(name) for name in [
    'inference_engine_ir_reader',
    'inference_engine_onnx_reader',
    'inference_engine_preproc',
    'inference_engine_legacy',
    'inference_engine_lp_transformations',
    'MKLDNNPlugin',
]]

data += [libs_dir + '/plugins.xml']

# For Linux these libraries are resolved by auditwheel
if sys.platform == 'win32':
    data += [os.environ['TBB_DIR'] + '/../bin/tbb.dll']
    data += [os.environ['TBB_DIR'] + '/../bin/tbbmalloc.dll']
    data += [libs_dir + '/inference_engine.dll']
    data += [libs_dir + '/inference_engine_transformations.dll']
    data += [libs_dir + '/ngraph.dll']

    with open(libs_dir + '/python_api/python{}/openvino/__init__.py'.format(py_version), 'wt') as f:
        f.write("import os\n")
        f.write("os.environ['PATH'] = os.path.dirname(__file__) + '..\\..\\experimental_openvino_python.libs' + os.pathsep + os.environ['PATH']")


setup(name='experimental-openvino-python',
      version=os.environ['VERSION'],
      author='Dmitry Kurtaev',
      url='https://github.com/dkurt/openvino-python-manylinux/',
      ext_modules=extensions,
      cmdclass={"build_ext": copy_ext},
      packages=['openvino', 'openvino.inference_engine'],
      package_dir={'openvino': libs_dir + '/python_api/python{}/openvino'.format(py_version)},
      data_files=[('../../experimental_openvino_python.libs', data)],
      install_requires=['numpy'],
)
