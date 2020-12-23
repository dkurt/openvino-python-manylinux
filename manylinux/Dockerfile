FROM quay.io/pypa/manylinux2014_x86_64

ARG VERSION
ARG OPENVINO_BRANCH

# Install Cython
RUN for ver in cp36-cp36m cp37-cp37m cp38-cp38 cp39-cp39; do \
        /opt/python/${ver}/bin/python -m pip install cython; \
    done

# Build libpython3.x.so
RUN yum install -y zlib-devel && \
    for ver in cp36-cp36m cp37-cp37m cp38-cp38 cp39-cp39; do \
        full_ver=$(/opt/python/${ver}/bin/python -c "import platform; print(platform.python_version())"); \
        curl https://www.python.org/ftp/python/${full_ver}/Python-${full_ver}.tgz -o Python-${full_ver}.tgz; \
        tar -xf Python-${full_ver}.tgz && cd Python-${full_ver}; \
        ./configure --enable-optimizations --enable-shared > /dev/null; \
        make altinstall -j$(nproc) > /dev/null; \
        cd /; \
    done

RUN git clone --depth 1 -b ${OPENVINO_BRANCH} https://github.com/openvinotoolkit/openvino/ && \
    cd openvino && \
    git submodule update --init --recursive && \
    mkdir build

RUN cd openvino/build && \
    for ver in cp36-cp36m cp37-cp37m cp38-cp38 cp39-cp39; do \
        full_ver=$(/opt/python/${ver}/bin/python -c "import platform; print(platform.python_version())"); \
        minor_ver=${ver:8}; \
        cmake .. \
            -DCMAKE_BUILD_TYPE=Release \
            -DENABLE_VPU=OFF \
            -DENABLE_CLDNN=OFF \
            -DENABLE_SAMPLES=OFF \
            -DENABLE_OPENCV=OFF \
            -DENABLE_CPPLINT=OFF \
            -DENABLE_PYTHON=ON \
            -DPYTHON_EXECUTABLE="/opt/python/${ver}/bin/python" \
            -DPython3_EXECUTABLE="/opt/python/${ver}/bin/python" \
            -DPYTHON_INCLUDE_DIR="/opt/python/${ver}/include/python3.${minor_ver}/" \
            -DPYTHON_LIBRARY="/Python-${full_ver}/libpython3.${minor_ver}.so" && \
        make -j$(nproc); \
    done

ENV VERSION=$VERSION

ADD setup.py /

RUN export LD_LIBRARY_PATH=/openvino/bin/intel64/Release/lib/:$LD_LIBRARY_PATH && \
    export OPENVINO_LIBS_DIR=/openvino/bin/intel64/Release/lib && \
    export TBB_DIR=/openvino/inference-engine/temp/tbb/cmake/ && \
    mkdir /wheels && \
    for ver in cp36-cp36m cp37-cp37m cp38-cp38 cp39-cp39; do \
        mkdir /wheel_${ver} && cd /wheel_${ver}; \
        /opt/python/${ver}/bin/python /setup.py build bdist_wheel; \
        auditwheel repair dist/experimental_openvino_python-${VERSION}-${ver}-linux_x86_64.whl; \
        cp wheelhouse/experimental_openvino_python-${VERSION}-${ver}-manylinux2014_x86_64.whl /wheels; \
    done
