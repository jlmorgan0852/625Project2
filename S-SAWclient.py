#import modules 
import socket
import time

def server():
  # create udp socket 
   s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s_socket.bind(('127.0.0.1', 20001))

   print (f"Server listening...")

  #initialize sequence number and show that entire file receieved is false 
   seq_no = 0
   file_received = False

  # while it is false: take data from client, decode it, 
   while not file_received: 
    data, c_addre = s_socket.recvfrom(1024) #sizr of data allowed to come in 
   

    #decdoe it, get the sequence number and data seperate
    full_data = data.decode()
    data_rcv = full_data.split(":")
    seq_no_recv = data_rcv[0]
    message=data_rcv[1]

    # print that the data has been receieved 
    print(f"Received data from {c_addre}: \n Sequence number: {seq_no_recv}\n Data: {message}\n")
       
  # send ack back to client 
    ack_msg = f"ACK {seq_no_recv}.encode()"    
    s_socket.sendto(ack_msg.encode(), c_addre)          
        
  # write info to second txt 
    with open('COSC635_P2_DataReceived.txt', 'a') as file:
      file.write(f"Segment Sequence Number {seq_no_recv} : \n{message}\n")

    seq_no += 1

    
    
if __name__ == "__main__":
   server()
