import numpy as np
import tifffile
from xml.etree.ElementTree import Element, SubElement, tostring

def create_custom_ome_tiff(file_path):
    
    image_data = np.random.randint(0, 256, (512, 512, 3), dtype=np.uint8) # 512 x 512 pixels, 3 channels - RGB

    # OME-XML metadata
    ome = Element('OME', xmlns='http://www.openmicroscopy.org/Schemas/OME/2016-06') # <OME> element created
    image = SubElement(ome, 'Image', ID='Image:0') # <Image> added as child element of <OME>
    pixels = SubElement(image, 'Pixels', DimensionOrder='XYCZT', ID='Pixels:0', # <Pixels> added as child element of <Image>
                        SizeX='512', SizeY='512', SizeZ='1', SizeC='3', SizeT='1',
                        Type='float')
    for c in range(3):
        SubElement(pixels, 'Channel', ID=f'Channel:0:{c}', SamplesPerPixel='1') # Adds <Channel> as child element to <Pixels>
    
    ome_xml = tostring(ome).decode('utf-8')

    # Save the image data with OME-XML metadata
    with tifffile.TiffWriter(file_path) as tif:
        tif.write(image_data, description=ome_xml, photometric='rgb')

# Path to save the custom OME-TIFF file
file_path = 'custom_ome_tiff.ome.tif'

create_custom_ome_tiff(file_path)



