# Create scatter plot as a function of files and dates
# Markers will represent authors and must be uniquely colored
import matplotlib.pyplot as plt
import json
import numpy as np
import datetime

# Open file created by my authorsFileTouches.py script
with open('Jayson_scatterplotData.txt', 'r') as file:
    # Grab dictionary info generated in authorsFileTouches.py
    dictfiles = json.load(file)

    # Variables for scatter plot
    initDate = datetime.datetime.fromisoformat('2015-06-19T00:00:00Z')
    xData = []      # x axis data
    yData = []      # y axis data
    fig = plt.figure()  # Create new figure
    ax = plt.gca()      # Get current axes

    # Iterate through each author's data (filenames and dates)
    for author in dictfiles.keys():
        # Get filenames and date data for current author
        for data in dictfiles[author]:
            # Add filename to xData
            for filename in data.keys():
                xData.append(filename)

            # Clean up date data and add to yData
            for date in data.values():
                date = datetime.datetime.fromisoformat(date)
                date = date - initDate
                yData.append(date.days)      # Contains date (days)

        # Plot all of the data points for the current author
            # label=author - consistent color for author
        ax.scatter(xData, yData, label=author)
        xData = []
        yData = []
    
    # Adjust labels and scale for axes, show figure
    ax.set_xlabel('file')
    ax.set_xscale('linear')
    ax.set_ylabel('days')
    ax.set_yscale('linear')
    plt.show()
