import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import json
from datetime import datetime


with open('commits.json', 'r') as file:
    data = json.load(file)

xValues = []
yValues = []
colors = []

#create a color for each author
author_colors = {author: color for author, color in zip(
    set(commit['author'] for commit in data), mcolors.TABLEAU_COLORS)}

# looping through each commit, and adding the new points to the plot data.
for commit in data:
    for i, file in enumerate(commit['files']):
        xValues.append(i + 1)  # File numbers: 1, 2, 3, ...

        # converting date to week #
        commit_date = datetime.strptime(commit['date'], '%Y-%m-%dT%H:%M:%SZ')
        week_number = commit_date.strftime('%U')  # Week number (Sunday as first day of the week)
        yValues.append(week_number)

        # Assign a color based on the author
        author_color = author_colors[commit['author']]
        colors.append(author_color)

# Create the scatter plot instance
plt.figure(figsize=(10, 6))
scatter = plt.scatter(xValues, yValues, c=colors)

# Add labels and title
plt.xlabel('File')
plt.ylabel('Week Number')
plt.title('File vs Week Number with Author Coloring')

handles, labels = scatter.legend_elements()
plt.show()