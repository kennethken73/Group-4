import csv
import matplotlib.pyplot as plt
import math
from datetime import datetime

CSV_FILENAME = "data/commit_data.csv"

def parse_date(date_str):
    date_str = date_str.replace("Z", "")
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

def main():
    commits = []
    with open(CSV_FILENAME, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dt = parse_date(row["Date"])
            commits.append({
                "filename": row["Filename"],
                "author": row["Author"],
                "date_dt": dt
            })

    earliest = min(c["date_dt"] for c in commits)
    for c in commits:
        c["weeks_since_start"] = (c["date_dt"] - earliest).days / 7.0

    files = sorted({c["filename"] for c in commits})
    file_index = {f: i for i, f in enumerate(files)}
    authors = sorted({c["author"] for c in commits})
    cmap = plt.cm.get_cmap("tab20", len(authors))
    color_map = {a: cmap(i) for i, a in enumerate(authors)}

    plt.figure(figsize=(10, 7))
    for c in commits:
        x = file_index[c["filename"]]
        y = c["weeks_since_start"]
        plt.scatter(x, y, color=color_map[c["author"]], alpha=0.8, s=30)

    plt.xlabel("File")
    plt.ylabel("Weeks")

    max_x = len(files) - 1
    plt.xticks(range(0, max_x + 1, 2))

    max_y = max(c["weeks_since_start"] for c in commits)
    max_y_rounded = int(math.ceil(max_y / 50.0) * 50)
    plt.yticks(range(0, max_y_rounded + 1, 50))

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
    