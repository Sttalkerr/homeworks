import os
import tarfile
import json
import xml.etree.ElementTree as ET
import platform

def read_config(config_path):
    tree = ET.parse(config_path)
    root = tree.getroot()

    config = {
        "hostname": root.find('hostname').text,
        "vfs_path": root.find('vfs_path').text,
        "log_path": root.find('log_path').text
    }
    return config

def extract_vfs(tar_path, extract_to):
    # Проверка существования файла
    if not os.path.isfile(tar_path):
        print(f"File not found: {tar_path}")
        return
    try:
        with tarfile.open(tar_path, 'r:*') as tar_ref:  
            tar_ref.extractall(extract_to)
            print(f"Extracted {tar_path} to {extract_to}")
    except Exception as e:
        print(f"Error extracting {tar_path}: {e}")

def list_directory(path):
    try:
        files = os.listdir(path)
        if files:
            print("  ".join(files))  # Выводим файлы в одну строку с пробелами
        else:
            print("Directory is empty.")
    except FileNotFoundError:
        print("Directory not found.")

def change_directory(path, start_dir):
    try:
        new_path = os.path.abspath(os.path.join(os.getcwd(), path))
        if not new_path.startswith(start_dir):
            return "Cannot go outside the starting directory."
        os.chdir(new_path)
        return os.getcwd()
    except FileNotFoundError:
        return "Directory not found."

def log_command(log_file, command):
    with open(log_file, 'a') as log:
        json.dump({"command": command, "path": os.getcwd()}, log)
        log.write('\n')

def tail(file_path, n=10):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines[-n:]:
                print(line, end='')
            print('\n')
    except FileNotFoundError:
        print("File not found.")

def uname():
    system_info = platform.uname()
    print(f'System: {system_info.system}')
    print(f'Node Name: {system_info.node}')
    print(f'Release: {system_info.release}')
    print(f'Version: {system_info.version}')
    print(f'Machine: {system_info.machine}')
    print(f'Processor: {system_info.processor}')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def shell(config):
    extract_vfs(config["vfs_path"], "./vfs")
    log_file = config["log_path"]
    start_dir = os.getcwd()
    command_history = []

    if not os.path.exists(log_file):
        with open(log_file, 'w') as log:
            pass

    while True:
        command = input(f"{config['hostname']}:~$ ")

        if command == "exit":
            break
        elif command == "ls":
            list_directory(os.getcwd()) 
            log_command(log_file, command)
        elif command.startswith("cd "):
            path = command[3:]
            result = change_directory(path, start_dir)   
            log_command(log_file, command)
        elif command == "clear":
            clear()
            log_command(log_file, command)
        elif command == "uname":
            uname()
            log_command(log_file, command)
        elif command[:4] == "tail":
            path = command[5:-2]
            tr=int(command[-1])
            tail(path, tr)  
            log_command(log_file, command)
        else:
            print("Command not found.")

        command_history.append(command)

    with open(log_file, 'w') as log:
        log.truncate(0)

if __name__ == "__main__":
    config = read_config("config.xml")
    shell(config)