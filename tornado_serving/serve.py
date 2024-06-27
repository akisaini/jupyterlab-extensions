import tornado.ioloop
import tornado.web
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        file_path = 'custom_ome_tiff.ome.tif'
        if os.path.exists(file_path):
            self.set_header('Content-Type', 'image/tiff')
            with open(file_path, 'rb') as f:
                self.write(f.read())
        else:
            self.set_status(404)
            self.write("File not found")

def make_app():
    return tornado.web.Application([
        (r"/image", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()
