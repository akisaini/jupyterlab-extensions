from tornado import ioloop, web
import os

class MainHandler(web.RequestHandler):
    def get(self):
        # Path to the TIFF image 
        file_path = '/Users/sainia2/Documents/pj/forks/jupyterlab-extensions/tornado_serving/tmp/LuCa-7color_3x3component_data.ome.tif'

        if not os.path.exists(file_path):
            self.set_status(404)
            self.write("File not found")
            return

        file_size = os.path.getsize(file_path) # In bytes
        # file_size = 899328715 
        # Indicates the unit that can be used to define a range 
        self.set_header('Accept-Ranges', 'bytes')

        range_header = self.request.headers.get('Range', None)
        start = 732233728
        end = 732692480

        # Partial Content Status
        self.set_status(206)
        self.set_header('Content-Range', f'bytes {start}-{end}/{file_size}')

            
        with open(file_path, 'rb') as f:
            f.seek(start)
            chunk_size = 4096
            while start <= end:
                if end - start + 1 < chunk_size:
                    chunk_size = end - start + 1
                data = f.read(chunk_size)
                if not data:
                    break
                self.write(data)
                self.flush()
                start += chunk_size


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
