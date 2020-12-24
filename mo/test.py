import sys
import subprocess
import model_optimizer.mo_tf as mo

subprocess.run([sys.executable,
                mo.__file__,
                '--input_model', 'tensorflow_inception_graph.pb',
                '--input_shape', '[1,224,224,3]'],
               check=True)
