#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio LORA_SDR module. Place your Python package
description here (python/__init__.py).
'''
import os

# import pybind11 generated symbols into the lora_sdr namespace
#try:
    # this might fail if the module is python-only
#    from .lora_sdr_python import *
from .lora_sdr_swig import *

#except ModuleNotFoundError:
#    pass

# import any pure python here
#
from .lora_sdr_lora_tx import lora_sdr_lora_tx
from .lora_sdr_lora_rx import lora_sdr_lora_rx
