import os
from tornado import web, iostream, gen, ioloop

class DownloadHandler(web.RequestHandler):
    async def get(self, filename):
        # Define the chunk size for reading the file
        chunk_size = 1024 * 1024 * 1  # 1 MiB

        # Ensure the file exists
        if not os.path.exists(filename):
            self.set_status(404)
            self.write("File not found")
            return

        # Read and send the file in chunks
        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                try:
                    self.write(chunk)  # Write the chunk to the response
                    await self.flush()  # Send the chunk to the client
                except iostream.StreamClosedError:
                    # Client has closed the connection, break the loop
                    break
                finally:
                    del chunk
                    # Pause the coroutine to allow other handlers to run
                    await gen.sleep(0.000000001)  # 1 nanosecond

def make_app():
    return web.Application([
        (r"/download/(.*)", DownloadHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)  # Listen on port 8888
    print("Server started at http://localhost:8888")
    ioloop.IOLoop.current().start()
