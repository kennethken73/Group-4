##################################################################
# Author:       John Zaleschuk                                   #
# Date:         1/29/2025                                        #
# Program:      John_scatterplot.py                              #
# Description:  Processes data from John_authorsFileTouches.py   #
#               and plots it with distinct colors per author     #
##################################################################

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# use pandas to read csv file
file = 'data/file_rootbeer.csv'
data = pd.read_csv(file)

# converting messy date colomn to a nice format
data['Date'] = pd.to_datetime(data['Date'])
# finding the earliest date for 'week 0'
earliest_date = data['Date'].min()
# subtract all dates from earliest date then floor divide by 7
data['Week'] = (data['Date'] - earliest_date).dt.days // 7 

# get a list of unique files
unique_files = data['Filename'].unique()
# parse the unique files and assign an index for each one
index_files = {file: i for i, file in enumerate(unique_files)}
# map the non unique files with their respective file index
data['FileIndex'] = data['Filename'].map(index_files)

# get a list of unique authors
unique_authors = data['Author'].unique()
# create a colormap with colors for each author (if there are >20 authors the colors repeat)
colormap = cm.get_cmap('tab20', len(unique_authors))

plt.figure()
# for each unique author, plot all the data under that authors color
for i, author in enumerate(unique_authors):
    author_data = data[data['Author'] == author]
    plt.scatter(author_data['FileIndex'], author_data['Week'], color=colormap(i), label=author)


plt.xlabel('Files')
plt.ylabel('Weeks')
plt.title('Source File Commits From github.com/scottyab/rootbeer')
plt.legend(title='Authors')

plt.show()
