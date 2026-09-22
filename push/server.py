import socket 
import threading
# main thread
HOST='' #listen to all network interfaces on this machine
PORT=50007
clients=[]
clients_lock=threading.Lock()
def broadcast(message,exclude=None):
    with clients_lock: 
        # __enter__() gets called in clients_lock
        #__acquire__() gets called by __enter__() -> return true or false
        for client in clients:
            if client!=exclude:
                try:
                    client.sendall(message.encode()) 
                    #if a client b is gets disconnected from the socket list and it is still present in clients list 
                    #then it can cause a connectionResetError or brokenPipeError
                except:
                    pass     
                
def handle_client(conn,addr): # conn is the actual new socket created by os to communicate with that client
    print(f"Client connected {addr}")
    broadcast(f"Client {addr} has connected\n",exclude=conn)
    try:
        while True:
            data=conn.recv(1024)
            if not data:
                break
            message=data.decode()
            broadcast(f"Client {addr}: {message}\n",exclude=conn)
    except ConnectionResetError:#if client disconnects
        pass
     
    finally: #no matter what happens this will execute
        with clients_lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()
        
        print(f"Client dissconnected {addr}")
        
        broadcast(f"Client {addr} has disconnected")

def start_server():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) # when we close the server and immmediately restart it then it may happen we get a osError (address already in use) because tcp may keep the old connection due to time_wait, so SO.REUSEADDR that if a socket is stuck in time_wait use that
        server.bind((HOST,PORT))
        server.listen()
        print(f"Server listening on port {PORT}")
        while True:
            conn,addr=server.accept()
            with clients_lock:
                clients.append(conn)
            thread=threading.Thread(
                target=handle_client,
                args=(conn,addr) 
            ) # creates a thread object (second thread) for client target means whenever thread starts handle_client function is to be executed and as the handle_client expects the args: conn,addr we are giving that as well 
            thread.start() #thread starts executing from handle_client(conn,addr)
            
if __name__=="__main__":
    start_server()