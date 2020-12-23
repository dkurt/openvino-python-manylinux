import sys
import hashlib
from urllib.request import urlopen, Request
from openvino.inference_engine import IECore

MB = 1024 * 1024
BUFSIZE = 10 * MB

def get_hash(path):
    sha = hashlib.sha256()
    with open(path, 'rb') as f:
        sha.update(f.read())
    return sha.hexdigest()


def download_file(url, output, sha256):
    r = urlopen(url)

    d = dict(r.info())
    size = '<unknown>'
    if 'content-length' in d:
        size = int(d['content-length'])
    elif 'Content-Length' in d:
        size = int(d['Content-Length'])
    print('  %s %s [%s MB]' % (r.getcode(), r.msg, size))

    print('get', url)
    with open(output, 'wb') as f:
        sys.stdout.write('  progress ')
        sys.stdout.flush()
        buf = r.read(BUFSIZE)
        while buf:
            sys.stdout.write('>')
            sys.stdout.flush()
            f.write(buf)
            buf = r.read(BUFSIZE)
        sys.stdout.write('\n')

    downloaded_sha = get_hash(output)
    if downloaded_sha != sha256:
        raise Exception('Hash mismatch:\n expected:', sha256, '\ngot:', downloaded_sha)


download_file('https://download.01.org/opencv/2020/openvinotoolkit/2020.1/open_model_zoo/models_bin/1/face-detection-adas-0001/FP32/face-detection-adas-0001.bin',
              'face-detection-adas-0001.bin',
              '85a9334e031289692884e2aefbcb4ca401b003a3f25ff4dd0e669ba32f98cc0b')

download_file('https://download.01.org/opencv/2020/openvinotoolkit/2020.1/open_model_zoo/models_bin/1/face-detection-adas-0001/FP32/face-detection-adas-0001.xml',
              'face-detection-adas-0001.xml',
              '62b4bf7dead77e16a47428b541aa4f3c506cdf3c7e31a317aa75771dd907557c')

ie = IECore()
net = ie.read_network('face-detection-adas-0001.xml', 'face-detection-adas-0001.bin')
exec_net = ie.load_network(net, 'CPU')
