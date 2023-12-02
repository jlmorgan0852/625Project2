import socket
import random
import time

def server():
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #create socket
    s_socket.bind(('131.118.76.145', 20001)) #bind socket

    print("Server listening...")
    file_name = 'COSC635_P2_DataReceived.txt'
    seq_no = 0
    exp_seq_no = 0
    file_received = False

    #checks the file is not fully received
    while not file_received:
        data, c_address = s_socket.recvfrom(1024) #receives packet

        full_data = data.decode() #decodes all data in packet
        data_rcv = full_data.split(":") #splits data for message and sequence number
        seq_no_recv = int(data_rcv[0]) #obtains sequence number
        message = data_rcv[1] #obtains message

        print(f"Received data from {c_address} \n Sequence number: {seq_no_recv}\n Data: {message} \n") #prints address received from, seuqence number, and message
        
        #checks the correct sequence number was sent and handle aknowledgment
        if seq_no_recv == exp_seq_no: 
            ack_msg = f"ACK {seq_no_recv}" #acknoledgment to send
            s_socket.sendto(ack_msg.encode(), c_address)  #sends ack

            with open(file_name, 'a') as file: #opens files
                file.write(f"Segment Sequence Number {seq_no_recv}: \n{message}\n") #writes sequence number and message to file
            #increase seq no and expected seq no by 1
            seq_no += 1
            exp_seq_no +=1
        else: #handles out of order packet with no correction
            print(f"Out-of-order segment {seq_no_recv}")


    
if __name__ == "__main__":
    server()