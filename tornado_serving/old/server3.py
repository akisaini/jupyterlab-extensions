from tornado import ioloop, web
import numpy as np
from tifffile import TiffFile, imsave
import os

# Path to the TIFF image
file_path = '/Users/sainia2/Documents/pj/forks/jupyterlab-extensions/tornado_serving/tmp/LuCa-7color_3x3component_data.ome.tif'

# Load the TIFF image into a NumPy array
with TiffFile(file_path) as tif:
    image_array = tif.asarray()

# Preprocess different levels (example: downsampled versions)
levels = {
    'level_1': image_array,
    'level_2': image_array[::2, ::2],  # Downsampled by factor of 2
    'level_3': image_array[::4, ::4]   # Downsampled by factor of 4
}

# Create memory-mapped files for each level
level_memmaps = {}
for level, array in levels.items():
    level_file_path = f'/tmp/{level}.dat'  # File path for the memory-mapped file
    
    # Create a memory-mapped file
    memmap = np.memmap(level_file_path, dtype=array.dtype, mode='w+', shape=array.shape)
    
    # Write the array data to the memory-mapped file                                                                               
    memmap[:] = array[:]
    
    # Flush changes to disk and set in dictionary   
    memmap.flush()
    level_memmaps[level] = memmap


class MainHandler(web.RequestHandler):
    def get(self):
        # Get the requested level from the query parameters
        level = self.get_argument('level', 'level_1')
        
        # Catch invalid levels
        if level not in levels:
            self.set_status(400)
            self.write(f"Invalid level: {level}")
            return
        
        # Serve the requested byte range if a Range header is present
        range_header = self.request.headers.get('Range', None)
        if range_header:
            print(f"Received Range Header: {range_header}")  
            byte_range = range_header.split('=')[1]
            start, end = byte_range.split('-')
            start = int(start)
            end = int(end) 

            # Calculate the portion of the image array to be saved as TIFF
            portion = level_memmaps[level]
            total_size = level_memmaps[level].nbytes

            # Save the portion as a new TIFF file
            output_path = f'/tmp/portion_{level}.tif'
            imsave(output_path, portion)

            # Read the TIFF file and send it as response
            with open(output_path, 'rb') as f:
                chunk = f.read()

            # chunk, total_size = get_image_level_portion(level, start, end)

            print(f"Serving bytes {start} to {end} of {total_size}")  

            self.set_status(206)
            self.set_header('Content-Range', f'bytes {start}-{end}/{total_size}')
            self.set_header('Content-Length', len(chunk))
            self.set_header('Accept-Ranges', 'bytes')
            
            self.write(chunk)
            self.flush()
        else:
            # Serve the entire image level if no Range header is present as TIFF bytes
            array = level_memmaps[level]
            total_size = array.nbytes
            self.set_status(200)
            self.set_header('Content-Type', 'image/tiff')
            self.set_header('Content-Length', total_size)
            self.write(array.tobytes())
            self.flush()

def make_app():
    return web.Application([
        (r"/image", MainHandler),
    ])

def start_server():
    app = make_app()
    app.listen(8889)
    print("Tornado server is running at http://localhost:8889/image")
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    start_server()
