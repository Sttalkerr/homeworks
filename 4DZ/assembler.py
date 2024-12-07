import csv
import struct
import sys

def log_to_csv(data, filename='log.csv'):
    """Записывает данные в CSV файл."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow([row])
            writer.writerow(data[row])
            writer.writerow('\n')

def assemble_line(line):
    COMMANDS = {
        "LOAD_CONST": 0xEF,
        "READ_MEM": 0x2E,
        "WRITE_MEM": 0xF4,
        "NOT": 0x2A,
    }
    binary_command = []

    tokens = line.split()
    command_type = tokens[0]
    A = int(tokens[1])  
    B = int(tokens[2]) 

    if command_type == 'LOAD_CONST':  # Загрузка константы
        binary_command.append(A | 0x80)
        binary_command.append(B//2)
        binary_command.append(A >> 16)
        binary_command.append(A >> 8 & 0xFF)
        binary_command.append(0x00)

    elif command_type == 'READ_MEM':  # Чтение значения из памяти
        binary_command.append(A)
        binary_command.append(B//2)
        binary_command.append(A >> 16)
        binary_command.append(A >> 8 & 0xFF)
        binary_command.append(0x00)

    elif command_type == 'WRITE_MEM':  # Запись значения в память
        binary_command.append(A | 0x80)
        binary_command.append(B//2)
        binary_command.append(A >> 16)
        binary_command.append(A >> 8 & 0xFF)
        binary_command.append(0x00)

    elif command_type == 'NOT':  # Бинарная операция "!="
        binary_command.append(A)
        binary_command.append((B//2) &0XFF)
        binary_command.append((B//2) >> 8)
        binary_command.append(A >> 8 & 0xFF)
        binary_command.append(0x00)

    return binary_command

def assemble(file_path):
    bin_code = []
    log = {}

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                cmd_bytes = assemble_line(line)
                bin_code.extend(cmd_bytes)
                log[line] = [f"0x{byte:02X}" for byte in cmd_bytes]
                print(log[line])
    return bin_code, log    


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("[ Usage: python assembler.py input.asm output.bin log.csv ]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_bin_file = sys.argv[2]
    log_file = sys.argv[3]

    bin_code, log = assemble(input_file)
    with open(output_bin_file, 'w') as binf:
        binf.write(", ".join([f"0x{byte:02X}" for byte in bin_code]))
    log_to_csv(log)

    with open('log.csv', 'r') as file:
        filedata = file.read()

    filedata = filedata.replace('"', '')
    with open('log.csv', 'w') as file:
        file.write(filedata)
