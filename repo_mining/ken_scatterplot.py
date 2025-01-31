## per instructions, following recommendations at
## https://stackoverflow.com/questions/8202605/how-to-color-scatter-markers-as-a-function-of-a-third-variable

from ken_authorsFileTouches import getCommitRecord, printCommitRecord
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.ticker as ticker

# function:populateData
#########################################################################
def populateData():
 commit_record = getCommitRecord()
 x = [] # file by numberID of the commit file
 y = [] # project's year-day of the commit
 id = [] # who done it. TODO rename. inconsistent with id naming convention in ken_authors...py
 # as suggested by google for a list of matplotlib colors
 color_list = ['white', 'blue', 'yellow', 'red', 'green', 'purple',
               'pink', 'orange', 'cyan', 'magenta', 'black']
 legend = ['None:white', 'Ken:blue', 'Adam:yellow', 'Michael:red', 'Parham:green', 'Kevin:purple',
           'Hardy:pink', 'Tanner:orange', 'Jayson:cyan', 'Richard:magenta', 'John:black']

 for c in commit_record:
 ### x-row == files. If 39 files, then tick-marks for x are 0-38.
 # x = np.random.random(10)
  x.append(c.get("id"))  # identified unique files, tagged by an increasing number
  # y.append(c.get("day")) # project day
  y.append(c.get("hour")) # project hour

  person = str(c.get("contributor"))
  person_id = 0
  # TODO find a better way to do this
  match person:
   # case "None" person_id = 0
   case "Ken Harvey" | "kennethken73":             # 1
    person_id = 1
   case "Adam Hamou" | "AdamoHamou":               # 2
    person_id = 2
   case "Michael Soffer" | "michaelsoffer":        # 3
    person_id = 3
   case "Parham Pahlavan" | "RISINGCHART719":      # 4
    person_id = 4
   case "Kevin Ramos" | "Kemoshu":                 # 5
    person_id = 5
   case "Hardy F." | "hhrh":                       # 6
    person_id = 6
   case "tannerdonovan" | "overperformer":         # 7
    person_id = 7
   case "Jayson Kirchand-Patel" | "Kirchpa":       # 8
    person_id = 8
   case "Richard Vargasan" | "richvar":            # 9
    person_id = 9
   case "John Zaleschuk" | "John-Zaleschuk":       # 10
    person_id = 10

  id.append(person_id)

 commit_file_count = max(x)
 print(x)
 print('---')
 print(y)
 print('---')
 print(id)
# https://www.geeksforgeeks.org/how-to-create-a-scatter-plot-with-several-colors-in-matplotlib/
#########################################################################
#########################################################################
# Fourth plot rewrite
 # person_data as a list of lists, where list[1] are the data points for ken
 # then scatterplot those, and re-loop

 # Gather Data-points for each individual (based on the id[] array)
 # Set this way for easier access later (by name)
 none_data = [[], []]
 ken_data = [[], []]
 adam_data = [[], []]
 michael_data = [[], []]
 parham_data = [[], []]
 kevin_data = [[], []]
 hardy_data = [[], []]
 tanner_data = [[], []]
 jayson_data = [[], []]
 richard_data = [[], []]
 john_data = [[], []]
 group_data = [none_data, ken_data, adam_data, michael_data, parham_data, kevin_data,
               hardy_data, tanner_data, jayson_data, richard_data, john_data]           # 3d list

# per: https://stackoverflow.com/questions/522563/how-to-access-the-index-value-in-a-for-loop
#
 x_list = 0
 y_list = 1
 for idx, person in enumerate(id):      # idx starts at 0 normally. person is id[idx]
  group_data[person][x_list].append(x[idx])
  group_data[person][y_list].append(y[idx])


 # verify our lists are correct (verified correct)
 for person_idx, person_data in enumerate(group_data):
  print('person: ', person_idx)
  print('   x values: ', group_data[person_idx][x_list])
  print('   y values: ', group_data[person_idx][y_list])

 fig = plt.figure()
 ax = plt.subplot()
 # for each person_data, plt.scatter()
 for person_idx, person_data in enumerate(group_data):
  plt.scatter(person_data[x_list],
              person_data[y_list],
              marker='o',
              facecolors='none',
              edgecolors=color_list[person_idx],
              s=80,
              label=legend[person_idx])

 box = ax.get_position()
 ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
 ax.set_facecolor('grey')
 ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True)
 ax.xaxis.set_major_locator(plt.MaxNLocator(commit_file_count))
 ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

 plt.xlabel('File (as numbered)')
 plt.ylabel('At which hour')

 plt.show()

# legend-outside-of-plot help via:
# https://stackoverflow.com/questions/4700614/how-to-put-the-legend-outside-the-plot
#########################################################################
#########################################################################
populateData()



#  name_str = ''
#  if any(name_str in person for item in ken_names):
#   person_id = ken_id
#  if any(name_str in person for item in adam_names):
#   person_id = adam_id
#  if any(name_str in person for item in michael_names):
#   person_id = michael_id
#  if any(name_str in person for item in parham_names):
#   person_id = parham_id
#  if any(name_str in person for item in kevin_names):
#   person_id = kevin_id
#  if any(name_str in person for item in hardy_names):
#   person_id = hardy_id
#  if any(name_str in person for item in tanner_names):
#   person_id = tanner_id
#  if any(name_str in person for item in jayson_names):
#   person_id = jayson_id
#  if any(name_str in person for item in richard_names):
#   person_id = richard_id
#  if any(name_str in person for item in john_names):
#   person_id = john_id

#  ken_names = ["ken", "harvey", "sov"]
#  adam_names = ["adam", "hamou", "fazlavarx"]
#  michael_names = ["michael", "soffer", "msooff"]
#  parham_names = ["parham", "pahlavan", "risingchart"]
#  kevin_names = ["kevin", "ramos", "kemoshu", "evn._"]
#  hardy_names = ["hardy", "fenam", "_iwk", "hhrh"]
#  tanner_names = ["tanner", "donovan", "overperformer"]
#  jayson_names = ["jayson", "kirchand", "patel", "kirchj", "kirchpa"]
#  richard_names = ["richard", "vargason", "drachir", "richvar"]
#  john_names = ["john", "zaleschuk"]



#  #########################################################################
#  # Plot attempt 1
#  # color == person
#
#  fig, ax = plt.subplots()
#  ax.set_facecolor('lightgrey')
#
#  plt.scatter(x, y, c=id, cmap='tab10', s=500) # s is the size of the markers
#
# # plt.gray()
#  color_key = plt.colorbar()
#  color_key.set_ticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
#  color_key.set_ticklabels(['Ken', 'Adam', 'Michael', 'Parham',
#                           'Kevin', 'Hardy', 'Tanner', 'Jayson', 'Richard', 'John'])
#  plt.xlabel('File (as numbered)')
#  plt.ylabel('At which hour')
#
#  plt.show()
#
#
# #########################################################################

#########################################################################
# Second plot attempt

#  fig, ax = plt.subplots()
#  ax.set_facecolor('lightgrey')

#  plt.scatter(x, y, c=id, cmap=cmap, s=500) # s is the size of the markers

# # plt.gray()
#  color_key = plt.colorbar()
#  color_key.set_ticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
#  color_key.set_ticklabels(['None', 'Ken', 'Adam', 'Michael', 'Parham',
#                           'Kevin', 'Hardy', 'Tanner', 'Jayson', 'Richard', 'John'])
#  plt.xlabel('File (as numbered)')
#  plt.ylabel('At which hour')

#  plt.show()
#########################################################################


#########################################################################
# Third plot attempt
 # person_data as a list of lists, where list[1] are the data points for ken
 # then scatterplot those, and re-loop

 # Gather Data-points for each individual (based on the id[] array)
#  none_data = [[], []]
#  ken_data = [[], []]
#  adam_data = [[], []]
#  michael_data = [[], []]
#  parham_data = [[], []]
#  kevin_data = [[], []]
#  hardy_data = [[], []]
#  tanner_data = [[], []]
#  jayson_data = [[], []]
#  richard_data = [[], []]
#  john_data = [[], []]
#  group_data = [none_data, ken_data, adam_data, michael_data, parham_data, kevin_data,
#                hardy_data, tanner_data, jayson_data, richard_data, john_data]           # 3d list

# # per: https://stackoverflow.com/questions/522563/how-to-access-the-index-value-in-a-for-loop
# #
#  x_list = 0
#  y_list = 1
#  for idx, person in enumerate(id):      # idx starts at 0 normally. person is id[idx]
#   group_data[person][x_list].append(x[idx])
#   group_data[person][y_list].append(y[idx])


#  # verify our lists are correct (verified correct)
#  for person_n, person_data in enumerate(group_data):
#   print('person: ', person_n)
#   print('   x values: ', group_data[person_n][x_list])
#   print('   y values: ', group_data[person_n][y_list])

#  fig, ax = plt.subplots()
#  # for each person_data, plt.scatter()
#  for person_n, person_data in enumerate(group_data):
#   plt.scatter(person_data[x_list], person_data[y_list], c=color_list[person_n])

#  ax.legend()
#  plt.show()

#########################################################################
