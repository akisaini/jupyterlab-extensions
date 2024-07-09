import numpy as np
from bfio import BioWriter

width, height = 512, 512
channels = 3  # Number of channels
image = np.random.randint(0, 256, (height, width, 1, channels, 1), dtype=np.uint8)

output_path = "bfio_three_channel_image.ome.tif"

# Create and write the OME-TIFF file
with BioWriter(output_path, X=width, Y=height, Z=1, C=channels, T=1, dtype=np.uint8) as writer:
    # Write the image data to the writer
    writer[:] = image

print(f"Image saved to {output_path}")
