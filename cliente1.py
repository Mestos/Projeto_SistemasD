import socket
from sympy.solvers import solve

def eq_verify(eq):
    #for caractere in eq:  
    #    if caractere.isalpha():
    #        return False
    return True

def client_main_server():
    host = socket.gethostname()  # ip do servidor
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
        eq = input("---")   
        
        while True:
            if eq_verify(eq):
                break      
            else:
                eq = input("---")   
                
        client_socket.send(eq.encode())  # envia mensagem contendo uma equação
        resposta = client_socket.recv(1024).decode()
        print('Resultado: ' + resposta)  # mostra o resultado no terminal
    else:
        eq = client_socket.recv(1024).decode()
        sol = solve(eq)
        num = str(sol)
        client_socket.send(num.encode())
    
    client_socket.close()  # fecha conexão com o servidor principal       


if __name__ == '__main__':
    client_main_server()
    