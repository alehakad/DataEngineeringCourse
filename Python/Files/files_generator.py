import os

def generate_letter_files():
    os.mkdir("letters")
    os.chdir("letters")
    for letter in range(ord('A'), ord('Z')+1):
        with open(f"{chr(letter)}.txt", "w") as file:
            file.write(chr(letter))


if __name__ == "__main__":
    generate_letter_files()