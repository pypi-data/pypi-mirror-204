import os
import sys
#sys.path.insert(1, 'mammopy/segmentation_models')
sys.path.append(os.path.dirname(os.path.abspath('mammopy/segmentation_models')))
__version__ = "0.0.5"

from .mammopy import *
from .segmentation_models import *