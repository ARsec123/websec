from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import os

class MyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        if self.path == '/':
            self.path = '/xs_search.html'

        # Set the proper Content-type header
        if self.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        # Read the contents of the file and send it in the response
            filepath = self.translate_path(self.path)
            if os.path.isfile(filepath):
                with open(filepath, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_error(404, 'File not found')
        else:
            self.send_error(404, 'File not found')

    def translate_path(self, path):
        root = '.'  # Set the document root directory
        return os.path.abspath(os.path.join(root, path.lstrip('/')))

PORT = 20016
my_socket = ('localhost', PORT)

httpd = socketserver.TCPServer(my_socket, MyHandler)

print(f"Serving at http://localhost:{PORT}/")

httpd.serve_forever()
