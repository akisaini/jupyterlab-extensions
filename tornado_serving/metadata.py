import tifffile

ome_tiff_path = '/Users/sainia2/Documents/pj/forks/jupyterlab-extensions/tornado_serving/custom_ome_tiff.ome.tif'

# Open the OME-TIFF file
with tifffile.TiffFile(ome_tiff_path) as tif:
    # Print the OME-XML metadata
    ome_metadata = tif.ome_metadata
    print("OME-XML Metadata:\n", ome_metadata)

    # Print the IFD entries for each image in the TIFF file
    for page in tif.pages:
        print(f"Page {page.index}:")
        for tag in page.tags.values():
            print(f"  {tag.name}: {tag.value}")

    # Print additional details from the OME-TIFF file
    print("\nDetailed IFD entries:")
    for page in tif.pages:
        for tag in page.tags.values():
            print(tag)

