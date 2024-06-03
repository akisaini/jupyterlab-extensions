from tornado import ioloop, web
import os

class MainHandler(web.RequestHandler):
    def get(self):
        file_path = '/Users/sainia2/Documents/pj/forks/jupyterlab-extensions/tornado_serving/tmp/LuCa-7color_3x3component_data.ome.tif' 
        
        if os.path.exists(file_path):
            self.set_header('Content-Type', 'image/tiff')
            with open(file_path, 'rb') as f:
                while chunk := f.read(4096):
                    self.write(chunk)
                    self.flush()
        else:
            self.set_status(404)
            self.write("File not found")

def make_app():
    return web.Application([
        (r"/image", MainHandler),
    ])

def start_server():
    app = make_app()
    app.listen(8889)
    print("Tornado server is running at http://localhost:8889/image")
    ioloop.IOLoop.current().start()

start_server()
