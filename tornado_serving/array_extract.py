import numpy as np
import tifffile

def load_image(file_path):
    with tifffile.TiffFile(file_path) as tif:
        image_data = tif.asarray() # Reads the tiff data into a numpy array
    return image_data

ome_path = 'custom_ome_tiff.ome.tif'
numpy_ome_array = load_image(ome_path)
print(numpy_ome_array)