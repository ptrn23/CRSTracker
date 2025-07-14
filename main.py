import re

def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None

def show_raw_lines(lines, header_lines=5):
    print("Showing raw lines (after skipping header):\n")
    for i, line in enumerate(lines[header_lines:], start=header_lines):
        print(f"[{i}] {repr(line)}")

def parse_simplified_blocks(lines):
    classes = []
    current = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Detect class code (e.g., 5-digit number)
        if re.fullmatch(r'\d{5}', line):
            current = {'class_code': line}
            
            # Seek forward to course code
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines):
                current['course_code'] = lines[j].strip()
                j += 1

            # Seek forward to course title
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines):
                current['course_title'] = lines[j].strip()
                j += 1

            classes.append(current)
            i = j  # Continue from last consumed line
        else:
            i += 1
    return classes

def count_class_codes(lines):
    return sum(1 for line in lines if re.fullmatch(r'\d{5}', line.strip()))

def main():
    filepath = 'data.txt'
    lines = read_file(filepath)
    
    if lines:
        show_raw_lines(lines)

        expected_count = count_class_codes(lines)
        parsed_entries = parse_simplified_blocks(lines)

        print("\nParsed entries:")
        for entry in parsed_entries:
            print(entry)

        print(f"\n📊 Class Code Check: Expected {expected_count}, Parsed {len(parsed_entries)}")
        if len(parsed_entries) != expected_count:
            print("⚠️ Mismatch detected! Some classes may not have been parsed correctly.")
        else:
            print("✅ All class codes matched and parsed successfully.")
    else:
        print("Failed to read the file.")

if __name__ == '__main__':
    main()