import http.server
import ssl

server_address = ('127.0.0.1', 8000)
handler = http.server.SimpleHTTPRequestHandler
httpd = http.server.HTTPServer(server_address, handler)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("Serving on https://127.0.0.1:8000")
httpd.serve_forever()
