import numpy as np
import tifffile
import matplotlib.pyplot as plt

def load_image(file_path):
    with tifffile.TiffFile(file_path) as tif:
        image_data = tif.asarray() # Reads the tiff data into a numpy array
    return image_data

