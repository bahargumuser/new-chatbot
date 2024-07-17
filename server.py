from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import json
from langchain.document_loaders import JSONLoader

# JSON dosyasının yolu
json_dataset_path = './responses.json'

# JSON dosyasını yüklemek için JSONLoader
loader = JSONLoader(json_dataset_path)
data = loader.load()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/get'):
            query_components = urlparse.parse_qs(urlparse.urlparse(self.path).query)
            user_message = query_components.get('msg', [None])[0]
            response_message = self.simple_bot_response(user_message)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response_message.encode('utf-8'))
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())

    def simple_bot_response(self, text):
        if text is None:
            return "Lütfen bir mesaj girin."
        
        # Search for the response in the loaded data
        for item in data['data']:
            if item['question'].lower() in text.lower():
                return item['response']
        
        return "Üzgünüm, bu konuda size yardımcı olamıyorum."

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()