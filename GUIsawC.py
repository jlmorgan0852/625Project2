import socket
import random
import time
import tkinter as tk
from tkinter import ttk
import customtkinter

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
root = customtkinter.CTk()
root.geometry("500x350")
root.title("UDP Client")

class UDPClientGUI(customtkinter.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(pady=20, padx=60, fill="both", expand=True) #window frame
        label = customtkinter.CTkLabel(master=self, text="Enter the percentage of lost packets [0-99]:", font=("Roboto", 12)) #label
        label.pack(pady=12, padx=10)
        self.loss_percentage_entry = customtkinter.CTkEntry(master=self) #entry line for user
        self.loss_percentage_entry.pack(pady=12, padx=10)

        button = customtkinter.CTkButton(master=self, text="Start", command=self.start_client)
        button.pack(pady=12, padx=10)

        #progessbar
        # self.progressbar = customtkinter.CTkProgressBar(master=self, width=160, height=20, border_width=5)
        # self.progressbar.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        # self.progressbar.set(value=0)

        #label for stats
        self.status_label = customtkinter.CTkLabel(master=self, text="")
        self.status_label.pack(pady=12, padx=10)

    # def update_bar(self, seq_no): #update progressbar
    #     progress_percentage = (seq_no / 400) * 100
    #     self.progressbar.set(progress_percentage)
    #     self.progressbar.configure(to=int(seq_no))

    def start_client(self):
        loss_percentage = int(self.loss_percentage_entry.get())
        self.status_label.configure(text=f"Sending with {loss_percentage}% packet loss simulation...")

        c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c_socket.settimeout(2)
        file_path = 'COSC635_P2_DataSent.txt'
        data_size = 500
        seq_no = 0

        start_time = time.time()

        packets_sent = 0
        packets_lost = 0

        with open(file_path, 'rb') as file:
            while True:
                random.seed(time.time())
                random_no = random.randint(0, 99)
                if random_no < loss_percentage:
                    print(f"Simulating packet loss for segment {seq_no}")
                    packets_lost += 1
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

                                # self.update_bar(seq_no)  #update_bar call
                                break
                    except socket.timeout:
                        print(f"Timeout waiting for acknowledgment. Resending Segment {seq_no}")
                        c_socket.sendto(f"{seq_no} :".encode() + data_segment, ('127.0.0.1', 20001))

        c_socket.close()

        end_time = time.time()
        transmission_time = end_time - start_time

        self.status_label.configure(text=f"File sent to server: {file_path}\n"
                                     f"Packets sent: {packets_sent}\n"
                                     f"Packets lost: {packets_lost}\n"
                                     f"Transmission time: {transmission_time:.2f} seconds")

if __name__ == "__main__":
    udp_client_gui = UDPClientGUI(root)
    root.mainloop()
