import subprocess
import platform
import sys
import os

directory = sys.argv[1] if len(sys.argv) > 1 else '.'

def kill_vite_processes():
    result = None
    if platform.system() == "Windows":
        result = subprocess.run(['taskkill', '/F', '/IM', 'node.exe'])
    else:
        result = subprocess.run(['pkill', '-f', 'vite'])
    if not result.stderr:
        print("subprocess result:", result)
    elif 'not found' in result.stderr:
        print("No node.exe processes found to kill. All good not to worry.")

kill_vite_processes()

vite_process = None

def start_vite_server():
    global vite_process
    command = 'npx vite'
    vite_process = subprocess.Popen(command, shell=True, cwd=directory)

if __name__ == "__main__":
    start_vite_server()
