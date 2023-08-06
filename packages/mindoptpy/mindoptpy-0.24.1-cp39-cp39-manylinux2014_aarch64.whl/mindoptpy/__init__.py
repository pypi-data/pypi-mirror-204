import os
import platform
import sys

module_path = os.path.abspath(os.path.dirname(__file__))
lic_path = os.path.join(module_path, '.libs')

os.environ['MINDOPT_HOME'] = module_path
os.environ['MINDOPT_LICENSE_PATH'] = lic_path

if platform.system() == "Windows":
    sys.path.append(os.path.join(module_path, 'win64-x86', 'lib'))

from .mindoptpy import *

