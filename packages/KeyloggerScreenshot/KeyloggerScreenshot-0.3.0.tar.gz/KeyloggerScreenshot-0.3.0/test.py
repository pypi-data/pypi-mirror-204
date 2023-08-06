import os
import subprocess

data = subprocess.check_output("tasklist")
str_data = str(data).split()
all_exe = [(exe.replace(r"K\\r\\n", "").replace(r"K\r\n", ""), str_data[idx+1]) for idx, exe in enumerate(str_data) if ".exe" in exe]
photo = []
for task, pid in all_exe:
    if task == "PhotosApp.exe":
        photo.append((task, pid))

if photo:
    os.system(f"taskkill /f /PID {photo[0][1]}")