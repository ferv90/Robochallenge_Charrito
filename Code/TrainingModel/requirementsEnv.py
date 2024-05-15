# opencv-python == 4.9.0
# numpy == 1.26.1
# pandas == 2.2.2
# matplotlib == 3.8.4
# scikit-learn == 1.4.2
# tensorflow == 2.16.1
# imgaug == 0.4.0
#
#   pip install numpy
#   pip install opencv-python
#   pip install pandas
#   pip install matplotlib
#   pip install scikit-learn
#   pip install tensorflow
#   pip install imgaug
############################################################################################ 
# Run this script to check if all the libraries are installed in the environment.
# If the libraries are not installed, install them before running the Training.py code.
############################################################################################

import cv2
import numpy
import pandas
import matplotlib
import sklearn
import imgaug
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow

print('Packages versions:')
print('opencv:', cv2.__version__)
print('numpy:', numpy.__version__)
print('pandas:', pandas.__version__)
print('matplot:', matplotlib.__version__)
print('scikit-learn:', sklearn.__version__)
print('tensor-flow:', tensorflow.__version__)
print('imgaug:', imgaug.__version__)
print("All libraries are imported successfully!")