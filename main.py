
def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None

def main():
    filepath = 'data.txt'
    raw_data = read_file(filepath)
    
    if raw_data:
        print("File loaded successfully\n")
    else:
        print("Failed to read the file.")

if __name__ == '__main__':
    main()