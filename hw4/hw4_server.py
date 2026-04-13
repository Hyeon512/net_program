from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(10)

while True:
    c, addr = s.accept()
    print(f"Connected from {addr}")

    data = c.recv(1024)
    msg = data.decode()
    req = msg.split('\r\n')

    try:
        request_line = req[0]
        method, path, version = request_line.split()
        filename = path.lstrip('/')

        if filename == '':
            filename = 'index.html'

        print(f"Requested file: {filename}")
        try:
            if filename == 'index.html':
                f = open(filename, 'r', encoding='utf-8')
                mimeType = 'text/html; charset=utf-8'
                data = f.read()
                f.close()

                header = 'HTTP/1.1 200 OK\r\n'
                header += 'Content-Type: ' + mimeType + '\r\n'
                header += '\r\n'
                c.send(header.encode())

                c.send(data.encode())

            elif filename == 'iot.png':
                f = open(filename, 'rb')
                mimeType = 'image/png'
                data = f.read()
                f.close()

                header = 'HTTP/1.1 200 OK\r\n'
                header += 'Content-Type: ' + mimeType + '\r\n'
                header += '\r\n'
                c.send(header.encode())

                c.send(data)

            elif filename == 'favicon.ico':
                f = open(filename, 'rb')
                mimeType = 'image/x-icon'
                data = f.read()
                f.close()

                header = 'HTTP/1.1 200 OK\r\n'
                header += 'Content-Type: ' + mimeType + '\r\n'
                header += '\r\n'
                c.send(header.encode())

                c.send(data)

            else:
                raise FileNotFoundError

        except FileNotFoundError:
            response = 'HTTP/1.1 404 Not Found\r\n'
            response += '\r\n'
            response += '<HTML><HEAD><TITLE>Not Found</TITLE></HEAD>'
            response += '<BODY>Not Found</BODY></HTML>'
            c.send(response.encode())

    except Exception as e:
        print(f"Error: {e}")

    finally:
        c.close()
        print("Connection closed.")
