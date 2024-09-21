import socket
import subprocess
#from thresholds_trackbars import *
#from images_stack import *
#from count_shapes import *

first_time=1

server_ip = '0.0.0.0'  # Listen on all available interfaces
server_port = 5005

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

print(f"Server listening on {server_ip}:{server_port}")

conn, addr = server_socket.accept()
print(f"Connection from {addr}")
data=0

while(True):
    
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")
    data = conn.recv(1024)  # Buffer size
    print(conn.recv(1024).decode())
   # while(not(data)):
    #    data=conn.recv(1024)

   # print("Received data:", data.decode())

    if data.decode()=="FIRST_TASK" :
       # output=execute_count_shapes()
        #print(output)
        if(first_time):
            from count_shapes import *
            s="done"
            first_time=0
            conn.sendall(s.encode())
            print("Sent data to ESP32:", s)
        else :
            with open("count_shapes.py") as file:
                exec(file.read())
            print("done marokhra")    
            conn.sendall(s.encode())
            print("Sent data to ESP32:", s)
             

      



