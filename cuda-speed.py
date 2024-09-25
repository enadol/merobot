# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 18:06:53 2024

@author: enado
"""

import torch

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")
    
print("using", device, "device")