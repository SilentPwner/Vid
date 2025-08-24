# الخلية 1: تثبيت جميع التبعيات
# %%capture
!pip install diffusers transformers accelerate opencv-python spacy ftfy einops xformers mediapipe
!python -m spacy download en_core_web_sm
!sudo apt-get install ffmpeg

import torch
import cv2
import numpy as np
import spacy
from PIL import Image
import mediapipe as mp
from diffusers import StableDiffusionPipeline
from IPython.display import Video, display
import os