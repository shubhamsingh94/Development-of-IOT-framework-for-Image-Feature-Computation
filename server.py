import socket
import sys
import threading
import time
from queue import Queue

num_threads = 2
job_id = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []
users_connections = []
users_addresses = []

# Creating Socket


def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9001
        s = socket.socket()
    except socket.error as msg:
        print("Socket Creation Error: " + str(msg))

# Binding Socket


def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding Socket to port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
        socket_bind()

# Accepting Connections


def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while 1:
        try:
            conn, address = s.accept()
            # conn.send(str.encode(' '))
            data = str(conn.recv(20480), "utf-8")
            conn.setblocking(1)
            if(data == "Client"):
                all_connections.append(conn)
                all_addresses.append(address)
                print("Client Connection has been established: " + address[0])
            else:
                users_connections.append(conn)
                users_addresses.append(address)
                print("Users Connection has been established: " + address[0])
        except:
            print("Error accepting connections")

# Interactive Shell


def start_shell():
    print("--------------Command Prompt--------------\n")
    print("Valid Commands of command prompt : \n")
    print("1 -> 'list'  : lists all connections\n")
    print("2 -> 'select x'  :  make connections to the xth client\n")
    
    while True:
        cmd = input('MyShell> ')
        if cmd == 'quit':
            s.close()
            sys.exit()
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_user(cmd)
            if conn is not None:
                print("Server is ready to process user's data : ")
                take_input_from_user(conn)
        else:
            print("Command not Recognized")


def list_connections():
    result1 = ''
    result2 = ''

    for i, conn in enumerate(users_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del users_connections[i]
            del users_addresses[i]
            continue
        result1 += str(i) + '    ' + str(users_addresses[i][0]) + '    ' + str(users_addresses[i][1]) + '\n'
    print("---------Users--------"+'\n'+result1 + '\n')

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        result2 += str(i) + '    ' + str(all_addresses[i][0]) + '    ' + str(all_addresses[i][1]) + '\n'
    print("------------Clients--------"+'\n' + result2 + '\n')


# Get target
def get_user(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = users_connections[target]
        print('You are now connected to ' + str(users_addresses[target][0]))
        print(str(users_addresses[target][0]) + '> ', end='')
        return conn
    except:
        print('Not a valid Selection')
        return None



# Connect with the remote target
def take_input_from_user(conn):
    conn.send(str.encode('Server Ready!!!'))
    while True:
        try:
            print("Waiting for input from User!!!!")
            data =str(conn.recv(20480),'utf-8')
            print("Input from the user : " + data)
            if data == 'quit':
                break
            if len(str.encode(data)) > 0:
                processed_data = send_target_commands_to_client(data)
                conn.send(str.encode(processed_data))
                print("Processed data sent to the user : " + processed_data + "\n")
        except:
            print('Connection was lost')
            break



def send_target_commands_to_client(cmd):
    try:
        conn = all_connections[0]
        conn.send(str.encode(' '))
        conn.recv(20480)
        conn.send(str.encode(cmd))
        client_response = str(conn.recv(20480), "utf-8")
        return client_response
    except:
        print('Connection was lost')

# Creating threads


def create_threads():
    for _ in range(num_threads):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do the next job in the list (1 - handles connections, 2 - sends commands)


def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accept_connections()
        if x == 2:
            time.sleep(1)
            start_shell()
        queue.task_done()

# Each list item is a new job


def create_jobs():
    for x in job_id:
        queue.put(x)
    queue.join()


def main():
    create_threads()
    create_jobs()


main()