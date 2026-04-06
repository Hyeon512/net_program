from socket import *
s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 5000))
s.listen(5)
print('waiting...')
while True:
    client, addr = s.accept()
    print('connection from ', addr)
    while True:
        formula = client.recv(1024)
        if not formula:
            break
        try:    
            answer = answer = str(round(eval(formula.decode()), 1))
        except:
            client.send(b'Try again')
        client.send(answer.encode())
client.close()