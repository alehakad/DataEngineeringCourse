def read_first_n_lines(file_name:str, n_lines:int):
    with open(file_name, "r") as file:
        for i in range(n_lines):
            print(file.readline().strip())

if __name__ == "__main__":
    read_first_n_lines("lines_reader.py", 2)