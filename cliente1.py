import socket
from sympy.solvers import solve
from sympy import sympify
from sympy.core.sympify import SympifyError

def eq_verify(eq):
    try:
        sympify(eq)
        return True
    except SympifyError:
        return False

def client_main_server():
    host = '127.0.0.1'  # localhost
    port = 5000  # porta do socket

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # conecta-se ao servidor principal

    data = client_socket.recv(1024).decode()  # recebe mensagem do servidor perguntando tipo de cliente

    print('Received from server: ' + data)  # mostra a mensagem no terminal
    print("Escolha sua função: \n 0 - Provedor \n 1 - Receptor")
    tipo = (input(" --> "))  # digita uma mensagem identificando seu tipo
    
    while True:
        if tipo == "0" or tipo == "1":
            break
        else:
            print("Opção inválida")
            print("Escolha sua função: \n 0 - Provedor \n 1 - Receptor")
            tipo = (input(" --> "))  # digita uma mensagem identificando seu tipo
            
    while data != "Aprovado":
        client_socket.send(tipo.encode()) # envia mensagem ao servidor principal
        data = client_socket.recv(1024).decode()  # recebe mensagem do servidor perguntando tipo de cliente ou aprovando a mensagem
        print('Received from server: ' + data)  # mostra a mensagem no terminal
        
    if tipo == "1":
        eq=""
        while True:
            print("Digite a equação (ex: x**2 - 4 = 0 ou 3**4 + 6):")
            eq = input("--->")  
            if eq_verify(eq):
                break   
                
        client_socket.send(eq.encode())  # envia mensagem contendo uma equação
        resposta = client_socket.recv(1024).decode()
        print('Resultado: ' + resposta)  # mostra o resultado no terminal
    else:
        client_socket.send(" ".encode())
        eq = client_socket.recv(1024).decode()
        sol = solve(eq)
        num = str(sol)
        client_socket.send(num.encode())
    
    client_socket.close()  # fecha conexão com o servidor principal       


if __name__ == '__main__':
    client_main_server()
    
