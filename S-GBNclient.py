import socket;
import random;
import time;

def client():
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    file_name = 'COSC635_P2_DataSent.txt'
    data_size = 500 #size of data packet
    window_size = 4 #size of sliding window
    seq_no = 0 #current sequence number
    next_seq_no = 0 

    loss_percentage = int(input("Enter the percentage of lost packets [0-99]: "))
    start_time = time.time()
    packets_sent = 0
    packets_lost = 0
    with open(file_name, 'rb') as file:
        while True:
            #sliding window
            while next_seq_no < seq_no + window_size:
                random.seed(time.time())
                random_no = random.randint(0,99)
                #simulates packet loss
                if random_no < loss_percentage: #checks random nno less than loss percentage
                    print(f"Simulate Packet loss for {next_seq_no}") #simulates lost packt
                    packets_lost += 1 #add 1 to lost packet
                    time.sleep(1) 
                #sending packet
                else:
                    data = file.read(data_size) #reads data
                    if not data: #checks if data is left
                        break
                    c_socket.sendto(f"{next_seq_no} :".encode() + data, ('127.0.0.1', 20001)) #sennds seq no, message to server socket
                    packets_sent += 1 #increase packet sent
                    next_seq_no += 1 #increase next seq no
            #acknowledgment handling
            try:
                ackmsg, _ = c_socket.recvfrom(1024) #receives ack message
                ack_str = ackmsg.decode() #decodes ack message
                if ack_str.startswith("ACK"): #checks that it is an ack message
                    ack_no = int(ack_str.split()[1]) #splits message to obtain ack no
                    if ack_no >= seq_no: # compares ack no to sequences no
                        print(f"Ackloedgement Received for: {ack_no}")
                        seq_no = ack_no + 1
            except socket.timeout:
                print(f"Timeout occured.")
                next_seq_no = seq_no
            if seq_no == next_seq_no:
                break
    print(f"Entire {file_name} sent to server")

    c_socket.close()
    end_time = time.time()
    transmission_time = end_time - start_time

    print("\nTransmission Stats:")
    print(f"Packets sent: {packets_sent}")
    print(f"Packets lost: {packets_lost}")
    print(f"Transmission time: {transmission_time:.2f} seconds")
        


if __name__ == "__main__": 
    client()

    

