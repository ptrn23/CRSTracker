import os
import json
from datetime import datetime

def find_latest_snapshot(folder="snapshots"):
    files = [f for f in os.listdir(folder) if f.startswith("parsed_snapshot_") and f.endswith(".json")]
    if not files:
        print("No snapshot files found.")
        return None
    files.sort(reverse=True)
    return os.path.join(folder, files[0])

def load_snapshot(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def group_classes_by_prefix(data):
    grouped = {}
    for entry in data:
        prefix = " ".join(entry["course_code"].split()[:3])
        title = entry["course_title"]
        key = f"{prefix}: {title}"
        grouped.setdefault(key, 0)
        grouped[key] += 1
    return grouped

def generate_feed_text(grouped, timestamp):
    month = timestamp.strftime("%m").lstrip("0")
    day = timestamp.strftime("%d").lstrip("0")
    year = timestamp.strftime("%Y")
    hour = timestamp.strftime("%I").lstrip("0")
    minute = timestamp.strftime("%M")
    ampm = timestamp.strftime("%p")

    dt_str = f"{month}/{day}/{year} {hour}:{minute} {ampm}"

    feed = [f"PE CLASSES UPDATES — {dt_str}", ""]
    for key, count in sorted(grouped.items()):
        feed.append(f"• {key} ({count} class{'es' if count > 1 else ''})")
    return "\n".join(feed)

def save_feed(feed_text, output_file="feed.txt"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(feed_text)
    print(f"Feed saved to: {output_file}")

def main():
    latest_path = find_latest_snapshot()
    if not latest_path:
        return

    data = load_snapshot(latest_path)
    
    timestamp_str = os.path.basename(latest_path).replace("parsed_snapshot_", "").replace(".json", "")
    timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
    
    grouped = group_classes_by_prefix(data)
    feed_text = generate_feed_text(grouped, timestamp)
    save_feed(feed_text)

if __name__ == "__main__":
    main()