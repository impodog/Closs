import math
import os
import re
import sys
import threading
import traceback
import time

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"]="enable"
import warnings

import calca
import numpy as np
import pygame
import PygameCrew as pycr
import VerRect as vr

from .const import *

pygame.display.set_caption("Closs")
screen=pygame.display.set_mode((SCR_LENGTH,SCR_WIDTH),
                               #pygame.FULLSCREEN
                               )
pycr.Define_Screen(screen)
def _f():...
FunctionType=type(_f)