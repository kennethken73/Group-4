import csv
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

#function to calculate the week number relative to the project's start
def get_week_number(date_str, project_start_date):
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    days_since_start = (date_obj - project_start_date).days
    week_number = days_since_start // 7
    return week_number

#load data from a CSV file
file_path = "data/file_rootbeer_authors.csv"

#dictionary to store data for final scatter plot
data = defaultdict(lambda: {"authors": [], "dates": [], "touch_count": 0})

#reading the CSV
with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=',', quotechar='"') 
    for row in reader:
        print(row)
        filename = row["Filename"]
        authors = row["Authors"].split(", ")    # split authors into a list
        dates = row["Dates"].split(", ")        # split dates into a list
        touch_count = int(row["Touch Count"])   # convert touch count to an int

        data[filename] = {"authors": authors, "dates": dates, "touch_count": touch_count}

#determine the project start date so we can calculate weeks since start
all_dates = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ") for file in data.values() for date in file["dates"]]
project_start_date = min(all_dates)  #earliest date in the project

print(f"Project start date: {project_start_date}")

#prepare x-axis for scatter plot by assigning unique indices to each file
file_indices = {filename: idx for idx, filename in enumerate(data.keys())}

#assign unique colors to each author
unique_authors = set(author for file_data in data.values() for author in file_data["authors"])  # all unique authors
authors_colors = {}
num_authors = len(unique_authors)

#create a color palette with unique colors for each author
color_palette = plt.get_cmap("tab20", num_authors)
for idx, author in enumerate(unique_authors):
    authors_colors[author] = color_palette(idx)  #assign a unique color from the colormap

#create scatter plot of files vs. weeks since project start with authors' colors
fig, ax = plt.subplots(figsize=(12, 6))

for filename, file_data in data.items():
    x = file_indices[filename]  # File index as x-axis
    for author, date in zip(file_data["authors"], file_data["dates"]):
        y = get_week_number(date, project_start_date) # Weeks since start as y-axis
        ax.scatter(x, y, color=authors_colors[author], label=author, alpha=0.7)

#add legend with unique authors
handles, labels = ax.get_legend_handles_labels()
unique_legend = {label: handle for label, handle in zip(labels, handles)}  #avoid duplicate labels
ax.legend(unique_legend.values(), unique_legend.keys(), loc='upper right', bbox_to_anchor=(1.3, 1.05))

ax.set_xlabel("Files (Numeric Indices)")
ax.set_ylabel("Weeks Since Project Start")
ax.set_title("Scatter Plot of Files vs. Weeks with Authors' Colors")
plt.tight_layout()
plt.show()
