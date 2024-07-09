import tifffile

def parse_ome_tiff_metadata(file_path):
        with tifffile.TiffFile(file_path) as tif:
            # Extract metadata
            ome_metadata = tif.ome_metadata
            
            # Extract image series
            if len(tif.series) == 0:
                print("No image series found.")
                return None, None, None, None
            
            image_series = tif.series[0]  # For a single series image
            # Extract dimensions
            dimensions = image_series.shape
            
            # Get tile offsets and byte counts
            tile_offsets = []
            tile_bytecounts = []
            tiles = image_series.pages
            for tile in tiles:
                tile_offsets.append(tile.dataoffsets)
            for tile in tiles:
                tile_bytecounts.append(tile.databytecounts)

            # Flatten the offsets and byte counts
            flat_tile_offsets = []
            for sublist in tile_offsets:
                for offset in sublist:
                    flat_tile_offsets.append(offset)

            flat_tile_bytecounts = []
            for sublist in tile_bytecounts:
                for count in sublist:
                    flat_tile_bytecounts.append(count)
        
        return ome_metadata, dimensions, tile_offsets, tile_bytecounts, flat_tile_offsets, flat_tile_bytecounts


file_path = 'bfio_three_channel_image.ome.tif'
ome_metadata, dimensions, tile_offsets, tile_bytecounts, flat_tile_offsets, flat_tile_bytecounts = parse_ome_tiff_metadata(file_path)

if dimensions:
    print("Image Dimensions:", dimensions)
if tile_offsets:
    print("Tile Offsets:", tile_offsets)
else:
    print("No tile offsets found.")
if tile_bytecounts:
    print("Tile Byte Counts:", tile_bytecounts)
else:
    print("No tile byte counts found.")
if flat_tile_offsets:
    print("flat_tile_offsets:", flat_tile_offsets)
if flat_tile_bytecounts:
    print("flat_tile_bytecounts:", flat_tile_bytecounts)
