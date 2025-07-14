import os
import json
import re
from datetime import datetime
from collections import defaultdict

SNAPSHOT_DIR = "snapshots"
FEED_FILE = "feed.txt"

def load_snapshots():
    snapshots = sorted(
        [f for f in os.listdir(SNAPSHOT_DIR) if f.endswith(".json")],
        key=lambda f: os.path.getmtime(os.path.join(SNAPSHOT_DIR, f)),
        reverse=True
    )
    if len(snapshots) < 2:
        print("Not enough snapshots to compare.")
        return None, None
    return snapshots[1], snapshots[0]  # earlier, later

def load_data(filename):
    with open(os.path.join(SNAPSHOT_DIR, filename), 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def group_by_course(entries):
    grouped = defaultdict(list)
    for entry in entries:
        code = entry.get('course_code')
        if code:
            prefix = " ".join(code.split()[:3])
            grouped[prefix].append(entry)
    return grouped

def get_timestamp_from_filename(filename):
    match = re.search(r"(\d{8}_\d{6})", filename)
    if match:
        timestamp_str = match.group(1)
        try:
            return datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
        except ValueError:
            pass
    print(f"❌ Could not parse timestamp from filename: {filename}")
    return None

def format_datetime(dt):
    month = dt.strftime("%m").lstrip("0")
    day = dt.strftime("%d").lstrip("0")
    year = dt.strftime("%Y")
    hour = dt.strftime("%I").lstrip("0")
    minute = dt.strftime("%M")
    ampm = dt.strftime("%p")
    return f"{month}/{day}/{year} {hour}:{minute} {ampm}"

def summarize_changes(title, classes_by_code, suffix=""):
    lines = [f"[{title}]"]
    for course_code in sorted(classes_by_code.keys()):
        entries = classes_by_code[course_code]
        course_title = entries[0]['course_title']
        count = len(entries)
        suffix_part = f" {suffix}" if suffix else ""
        lines.append(f"• {course_code}: {course_title} ({count} class{'es' if count > 1 else ''}{suffix_part})")
    return "\n".join(lines)

def generate_comparison_feed(old_data, new_data, timestamp):
    old_grouped = group_by_course(old_data)
    new_grouped = group_by_course(new_data)

    old_keys = set(old_grouped.keys())
    new_keys = set(new_grouped.keys())

    # [NEW PE CLASSES]
    new_courses = {code: new_grouped[code] for code in new_keys - old_keys}

    # [ADDED PE CLASSES]
    added_courses = {}
    for code in new_keys & old_keys:
        old_count = len(old_grouped[code])
        new_count = len(new_grouped[code])
        if new_count > old_count:
            added_courses[code] = new_grouped[code][-1 * (new_count - old_count):]  # only show added entries

    # Build feed text
    feed = [f"PE CLASSES UPDATES — {format_datetime(timestamp)}", ""]

    if new_courses:
        feed.append(summarize_changes("NEW PE CLASSES", new_courses))
        feed.append("")

    if added_courses:
        lines = [f"[ADDED PE CLASSES]"]
        for code in sorted(added_courses):
            title = added_courses[code][0]['course_title']
            added_count = len(added_courses[code])
            lines.append(f"• {code}: {title} (+{added_count} new class{'es' if added_count > 1 else ''})")
        feed.extend(lines)
        feed.append("")

    return "\n".join(feed)

def main():
    earlier_file, later_file = load_snapshots()
    if not (earlier_file and later_file):
        return

    timestamp = get_timestamp_from_filename(later_file)
    if not timestamp:
        print("⚠️ Skipping: Unable to extract timestamp from filename.")
        return

    old_data = load_data(earlier_file)
    new_data = load_data(later_file)

    feed_text = generate_comparison_feed(old_data, new_data, timestamp)

    with open(FEED_FILE, 'w', encoding='utf-8') as f:
        f.write(feed_text)

    print(f"✅ Comparison feed saved to {FEED_FILE}")

if __name__ == "__main__":
    main()