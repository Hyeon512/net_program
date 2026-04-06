from socket import *
s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 5000))
while True:
    formula = input('formula : ')
    if formula == 'q':
        break
    s.send(formula.encode())
    print('answer:', s.recv(1024).decode())
s.close()