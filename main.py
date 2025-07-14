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
        
def parse_blocks(lines, header_lines=5):
    entries = []
    block_size = 14
    data_lines = lines[header_lines:]

    for i in range(0, len(data_lines), block_size):
        block = data_lines[i:i+block_size]

        if len(block) < block_size:
            print(f"Skipping incomplete block starting at line {i + header_lines}")
            continue

        try:
            class_code = block[0].strip()
            course_code = block[3].strip()
            course_title = block[4].strip()
            instructor = block[5].strip()
            credits = float(block[7].strip().strip('()'))
            schedule = block[10].strip()
            misc = block[13].strip().split('\t')

            delivery_mode = misc[0]
            slots = misc[1].split('/')
            available = int(slots[0].strip())
            total = int(slots[1].strip())
            demand = int(misc[2].strip())

            entry = {
                'class_code': class_code,
                'course_code': course_code,
                'course_title': course_title,
                'instructor': instructor,
                'credits': credits,
                'schedule': schedule,
                'delivery_mode': delivery_mode,
                'available': available,
                'total': total,
                'demand': demand
            }

            entries.append(entry)

        except Exception as e:
            print(f"Error parsing block starting at line {i + header_lines}: {e}")

    return entries

def main():
    filepath = 'data.txt'
    lines = read_file(filepath)

    if lines:
        entries = parse_blocks(lines)
        for e in entries:
            print(e)
    else:
        print("Failed to read the file.")

if __name__ == '__main__':
    main()