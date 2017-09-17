from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/hello'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = '<html><body>Hello!</body></html>'
            self.wfile.write(message)
            return
        else:
            self.send_error(404, 'File not found: {}'.format(self.path))

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                message_content = fields.get('message')

            output = '''
<html>
    <body>
        <h2>Okay, how about this:</h2>
        <h1>{}</h1>
        <form method="POST" enctype="multipart/form-data" action="/hello">
        <h2>What would you like me to say?</h2>
    </body>
</html>
'''.format(message_content[0])
            self.wfile.write(output)
            print output
        except:
            pass

def main():
    try:
        port = 8081
        server = HTTPServer(('localhost', port), WebServerHandler)
        print 'Web server running on port {}'.format(port)
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C, stopping web server'
        server.socket.close()

if __name__ == '__main__':
    main()