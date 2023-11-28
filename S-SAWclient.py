import socket
import random
import time

def client():
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c_socket.settimeout(2)
    file_path = 'COSC635_P2_DataSent.txt'
    data_size = 500
    seq_no = 0

    loss_percentage=int(input("Enter the percentage of lost packets [0-99]: "))
    start_time = time.time()
    packets_sent = 0
    packets_lost = 0 

    with open(file_path, 'rb') as file:
        while True:
            random.seed(time.time())
            random_no = random.randint(0,99)
            if random_no < loss_percentage:
                print(f"Simulating packet loss for segment {seq_no}")
                packets_lost +=1
                time.sleep(1)
                continue

            data_segment = file.read(data_size)
            if not data_segment:
                
                break
    
            c_socket.sendto(f"{seq_no} :".encode() + data_segment, ('127.0.0.1', 20001))
            packets_sent += 1

            while True:
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
                        print(f"Timeout waiting for acknowledgment. Resending Segment {seq_no}")
                        c_socket.sendto(f"{seq_no} :".encode() + data_segment, ('127.0.0.1', 20001))

    print(f"File sent to server: {file_path}")

    c_socket.close()

    end_time = time.time()
    transmission_time = end_time - start_time

    print("\nTransmission Stats:")
    print(f"Packets sent: {packets_sent}")
    print(f"Packets lost: {packets_lost}")
    print(f"Transmission time: {transmission_time:.2f} seconds")
   

if __name__ == "__main__":
   
    client()