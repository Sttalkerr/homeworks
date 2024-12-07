import sys
import csv

def interpret(input_bin_file, result_file, memory_range):
    memory = [0] * (memory_range[1] + 1)  
    results = []

    with open(input_bin_file, 'rb') as bin_f:
        while True:
            byte = bin_f.read(1)
            if not byte:
                break
            A = ord(byte)
            opcode = A
            B = int.from_bytes(bin_f.read(4), byteorder='little')
            if opcode == 111:
                results.append(B)

            elif opcode == 46: 
                if B < len(memory):
                    results.append(memory[B])
                else:
                    results.append("Error: Address out of range")

            elif opcode == 116:
                if B < len(memory):
                    memory[B] = A 
                else:
                    results.append("Error: Address out of range")


    with open(result_file, 'w', newline='') as result_f:
        csv_writer = csv.writer(result_f)
        w=0
        for result in memory:
            line=(str(w) + ' = ' + str(result))
            csv_writer.writerow(str(line))
            w+=1
        for result in memory:
            print(result)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python interpreter.py output.bin result.csv 0 350")
        sys.exit(1)

    input_bin_file = sys.argv[1] 
    result_file = sys.argv[2] 
    memory_start = int(sys.argv[3])
    memory_end = int(sys.argv[4])
    interpret(input_bin_file, result_file, (memory_start, memory_end))
    with open(result_file, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(',', '')
    with open(result_file, 'w') as file:
        file.write(filedata)