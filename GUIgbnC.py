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
root.title("GBN Client")

class GBNClientGUI(customtkinter.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(pady=20, padx=60, fill="both", expand=True)
        label = customtkinter.CTkLabel(master=self, text="Enter the percentage of lost packets [0-99]:", font=("Roboto", 12))
        label.pack(pady=12, padx=10)
        self.loss_percentage_entry = customtkinter.CTkEntry(master=self)
        self.loss_percentage_entry.pack(pady=12, padx=10)

        button = customtkinter.CTkButton(master=self, text="Start", command=self.start_client)
        button.pack(pady=12, padx=10)

        # self.progress_label = customtkinter.CTkLabel(master=self, text="Progress:")
        # self.progress_label.pack()

        # self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        # self.progress_bar.pack()

        self.status_label = customtkinter.CTkLabel(master=self, text="")
        self.status_label.pack(pady=12, padx=10)

    def start_client(self):
        loss_percentage = int(self.loss_percentage_entry.get())
        self.status_label.configure(text=f"Sending with {loss_percentage}% packet loss simulation...")

        c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c_socket.settimeout(2)
        file_name = 'COSC635_P2_DataSent.txt'
        data_size = 500
        window_size = 4
        seq_no = 0
        next_seq_no = 0

        start_time = time.time()

        packets_sent = 0
        packets_lost = 0

        with open(file_name, 'rb') as file:
            while True:
                while next_seq_no < seq_no + window_size:
                    random.seed(time.time())
                    random_no = random.randint(0, 99)
                    if random_no < loss_percentage:
                        print(f"Simulate Packet loss for {next_seq_no}")
                        packets_lost += 1
                        time.sleep(1)
                    else:
                        data = file.read(data_size)
                        if not data:
                            break
                        c_socket.sendto(f"{next_seq_no} :".encode() + data, ('127.0.0.1', 20001))
                        packets_sent += 1
                        next_seq_no += 1

                try:
                    ackmsg, _ = c_socket.recvfrom(1024)
                    ack_str = ackmsg.decode()
                    if ack_str.startswith("ACK"):
                        ack_no = int(ack_str.split()[1])
                        if ack_no >= seq_no:
                            print(f"Acknowledgement Received for: {ack_no}")
                            seq_no = ack_no + 1
                except socket.timeout:
                    print(f"Timeout occurred.")
                    next_seq_no = seq_no
                if seq_no == next_seq_no:
                    break

                # Update progress bar
                # progress_percentage = (seq_no / total_packets) * 100
                # self.progress_bar["value"] = progress_percentage
                # self.master.update_idletasks()

        c_socket.close()

        end_time = time.time()
        transmission_time = end_time - start_time

        self.status_label.configure(text=f"Entire {file_name} sent to server\n"
                                         f"Packets sent: {packets_sent}\n"
                                         f"Packets lost: {packets_lost}\n"
                                         f"Transmission time: {transmission_time:.2f} seconds")

if __name__ == "__main__":
    gbn_client_gui = GBNClientGUI(root)
    root.mainloop()
