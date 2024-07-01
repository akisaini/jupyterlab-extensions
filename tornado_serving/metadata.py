import tifffile

ome_tiff_path = '/Users/sainia2/Documents/pj/forks/jupyterlab-extensions/tornado_serving/custom_ome_tiff.ome.tif'

# Open file
with tifffile.TiffFile(ome_tiff_path) as tif:
    ome_metadata = tif.ome_metadata
    print("OME-XML Metadata:\n", ome_metadata)

    # Print IFD entries for each image
    for page in tif.pages:
        print(f"Page {page.index}:")
        for tag in page.tags.values():
            print(f"  {tag.name}: {tag.value}")

    # Print additional details
    print("\nDetailed IFD entries:")
    for page in tif.pages:
        for tag in page.tags.values():
            print(tag)

