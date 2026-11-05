import socket, threading

HOST, PORT = '127.0.0.2', 5000

def receber(s):
    while True:
        dados = s.recv(1024)
        if not dados:
            break
        print(f'\r{dados.decode()}\nVoce: ', end='')

nome = input('Seu nome: ')
with socket.socket() as s:
    s.connect((HOST, PORT))
    s.sendall(nome.encode())
    print('Conectado!')
    threading.Thread(target=receber, args=(s,), daemon=True).start()
    while (msg := input('Voce: ')) != 'sair':
        s.sendall(msg.encode())
    print('Desconectado')