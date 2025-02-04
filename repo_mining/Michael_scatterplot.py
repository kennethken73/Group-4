import matplotlib.pyplot as plt
import pandas as pd
import os
import datetime
import matplotlib.dates as mdates

# Load data from the CSV file
repo_name = "rootbeer"  # Change this to your repo name
file_path = f"data/authors_{repo_name}.csv"

if not os.path.exists(file_path):
    print(f"Error: File {file_path} not found. Run the authorsFileTouches script first.")
    exit(1)

# Read CSV into a Pandas DataFrame
df = pd.read_csv(file_path)

# Convert date strings to datetime objects
df["Date"] = pd.to_datetime(df["Date"])

# Determine the starting week (first commit in dataset)
start_date = df["Date"].min()
df["Weeks"] = (df["Date"] - start_date).dt.days // 7  # Convert days to weeks

# Assign colors to authors
authors = df["Author"].unique()
author_colors = {author: plt.cm.tab10(i % 10) for i, author in enumerate(authors)}

# Plot the scatter plot
plt.figure(figsize=(12, 6))
for author in authors:
    subset = df[df["Author"] == author]
    plt.scatter(subset["Weeks"], subset["Filename"], color=author_colors[author], label=author, alpha=0.7, edgecolors='black')

# Formatting the plot
plt.xlabel("Weeks since first commit")
plt.ylabel("Files")
plt.title(f"File Touches Over Time ({repo_name} Repository)")
plt.xticks(rotation=45)
plt.legend(title="Authors", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

# Show the plot
plt.show()
