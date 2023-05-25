from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import os
import urllib.parse
import time

class MyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        #parsed_path = urllib.parse.urlparse(self.path)
        #query_param = urllib.parse.parse_qs(parsed_path.query)

        #if parsed_path.path == '/search':
        if self.path.startswith('/search?keyword='):
            query_param = self.path.split('=')[1]
            #if 'keyword' in query_params:
            keyword = query_param.split('&')[0]
            start_time = time.time()
            matching_strings = search_keyword(keyword)
            end_time = time.time()
            time_taken = end_time - start_time
            
            response = '\n'.join(matching_strings) if matching_strings else 'Keyword not found.'
            response_length = len(response)
            response += '\nTime taken: {:.4f} seconds'.format(time_taken)
            
            self.send_response(200)
            self.send_header('\nContent-type', 'text/plain')
            self.send_header('Keyword length =', str(response_length))
            #self.send_header('Keyword length =', query_param) 
            #self.send_header('Keyword length =', keyword) 
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            if self.path == '/':
                self.path = '/xs_search_backup.html'

            # Set the proper Content-type header
            if self.path.endswith('.html'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

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

def search_keyword(keyword):
    keywords = ['hello', 'ciao', 'Building', 'are', 'cool', 'IBAN:DE123456789012123456']
    matching_strings = []

    for kw in keywords:
        matched_chars = ''
        prev_matched_char = ''
        for i in range(len(kw)):
            if i == 0 or prev_matched_char:
                if i < len(keyword) and keyword[i] == kw[i]:
                    time.sleep(0.1)
                    matched_chars += keyword[i]
                    prev_matched_char = True
                    #sleep(200)
                else:
                    prev_matched_char = False
        if matched_chars:
            matching_strings.append(matched_chars)

    return matching_strings

def run_server():
    PORT = 20018
    my_socket = ('localhost', PORT)
    httpd = socketserver.TCPServer(my_socket, MyHandler)
    print(f"Serving at http://localhost:{PORT}/")
    httpd.serve_forever()

run_server()