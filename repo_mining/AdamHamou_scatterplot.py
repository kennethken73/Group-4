import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# read file and load into dataframe
file_input = "data/authors_rootbeer.csv" 
df = pd.read_csv(file_input)

# Convert Date to datetime to properly sacale
df["Date"] = pd.to_datetime(df["Date"], utc=True)
project_start = df["Date"].min() # get min (start)

# Compute weeks since project started
df["WeeksSinceStart"] = ((df["Date"] - project_start).dt.days) // 7

# map files to indices for plotting
unique_files = df["Filename"].unique()
file_mapping = {file: i for i, file in enumerate(unique_files)}
df["FileIndex"] = df["Filename"].map(file_mapping)

# get different authors and assign random colors
authors = df["Author"].unique()
author_colors = {author: np.random.rand(3,) for author in authors}
df["Color"] = df["Author"].map(author_colors)

# Create the scatter plot
for author in authors:
    subset = df[df["Author"] == author]
    plt.scatter(subset["FileIndex"], subset["WeeksSinceStart"], 
                color=subset["Color"], label=author, alpha=0.7, s=50)

# Axes
plt.xlabel("File", fontsize=15)
plt.ylabel("Weeks Since Project Started", fontsize=15)

# increment weeks by 50
plt.yticks(range(df["WeeksSinceStart"].min(), df["WeeksSinceStart"].max() + 1, 50))

plt.grid(axis="y", linestyle="--", alpha=0.5) # show grid lines
plt.legend(fontsize=15) # legened to show when project started
plt.show()
