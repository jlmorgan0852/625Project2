|#import modules 
import socket
import random
import time

#define client function 
def client():
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #create socket 
    c_socket.settimeout(2) #time of 2 seconds if no data is recieved
    file_path = 'COSC635_P2_DataSent.txt' #location of file 
    data_size = 500 # each datagram packet is 500 bytes 
    seq_no = 0 # initalize seq num 0 

    loss_percentage=int(input("Enter the percentage of lost packets [0-99]: "))
    start_time = time.time() # record start time
    
    # initalization 
    packets_sent = 0
    packets_lost = 0 

    with open(file_path, 'rb') as file:
        while True:
            random.seed(time.time())
            random_no = random.randint(0,99)
            if random_no < loss_percentage: # compare random number to user input number 
                print(f"Simulating packet loss for segment {seq_no}")
                packets_lost +=1 # increment count of lost packet 
                time.sleep(1)
                continue

            data_segment = file.read(data_size) # read data segement in 
            if not data_segment:
                
                break
    
            # send packet with sequence number to server and increment send count 
            c_socket.sendto(f"{seq_no} :".encode() + data_segment, ('127.0.0.1', 20001)) 
            packets_sent += 1

            while True: # checking for acknowledgement number 
                    try:
                        ack_msg, _ = c_socket.recvfrom(1024)
                        ack_str = ack_msg.decode()
                        if ack_str.startswith("ACK"):
                            ack_number = int(ack_str.split()[1])
                            if ack_number == seq_no:
                                print(f"Acknowledgement received for Segment {seq_no}")
                                seq_no += 1
                                break 
                    except socket.timeout:
                        # if timeout, resend packet 
                        print(f"Timeout waiting for acknowledgment. Resending Segment {seq_no}") 
                        c_socket.sendto(f"{seq_no} :".encode() + data_segment, ('127.0.0.1', 20001))

    print(f"File sent to server: {file_path}") 

    c_socket.close()

    #recording time information 
    end_time = time.time()
    transmission_time = end_time - start_time


    #statistics of result 
    print("\nTransmission Stats:")
    print(f"Packets sent: {packets_sent}")
    print(f"Packets lost: {packets_lost}")
    print(f"Transmission time: {transmission_time:.2f} seconds")
   

if __name__ == "__main__":
   
    client()
