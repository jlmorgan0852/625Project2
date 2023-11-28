import socket
import time

def server():

   s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s_socket.bind(('127.0.0.1', 20001))

   print (f"Server listening...")

   seq_no = 0
   file_received = False

   while not file_received: 
    data, c_addre = s_socket.recvfrom(1024)
   

    full_data = data.decode()
    data_rcv = full_data.split(":")
    seq_no_recv = data_rcv[0]
    message=data_rcv[1]

    print(f"Received data from {c_addre}: \n Sequence number: {seq_no_recv}\n Data: {message}\n")
       
   
    ack_msg = f"ACK {seq_no_recv}.encode()"    
    s_socket.sendto(ack_msg.encode(), c_addre)          
        

    with open('COSC635_P2_DataReceived.txt', 'a') as file:
      file.write(f"Segment Sequence Number {seq_no_recv} : \n{message}\n")

    seq_no += 1

    
    
if __name__ == "__main__":
   server()
