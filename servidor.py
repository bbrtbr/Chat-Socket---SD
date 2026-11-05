import socket
import threading

HOST, PORT = '127.0.0.1', 5000
clientes = []
lock = threading.Lock()

def broadcast(msg, remetente=None):
    with lock:
        for c in clientes:
            if c is not remetente:
                try:
                    c.sendall(msg)
                except:
                    pass

def atender(conn, addr):
    nome = 'Anônimo'
    try:
        nome = conn.recv(1024).decode('utf-8', errors='ignore').strip() or 'Anônimo'
        with lock:
            clientes.append(conn)
        
        print(f'{addr} ({nome}) conectado')
        broadcast(f'{nome} entrou no chat\n'.encode(), remetente=conn)

        while True:
            dados = conn.recv(1024)
            if not dados:
                break
            texto = dados.decode('utf-8', errors='ignore')
            print(f'{nome} ({addr}): {texto}')
            broadcast(f'[{nome}]: {texto}'.encode(), remetente=conn)
    except:
        pass
    finally:
        with lock:
            if conn in clientes:
                clientes.remove(conn)
        conn.close()
        print(f'{nome} ({addr}) desconectado')
        broadcast(f'*** {nome} saiu do chat ***\n'.encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f'Servidor ativo em {HOST}:{PORT}')
    while True:
        conn, addr = s.accept()
        threading.Thread(target=atender, args=(conn, addr), daemon=True).start()