## See file: original_ken_authorsFileTouches.py for citations for help (ie google searches etc.)

import github
from datetime import date, datetime

# function:getCommitRecord
#######################################################################################################
def getCommitRecord():

 my_token =("")
 githubInstance = github.Github(my_token)

 # This *does* do an https request for this repo, complete with using credentials.
 # However, it then appears to use my local version of the repo.
 # I'm not sure if this is a hidden 'performance' thing or not.
 # I might simply need to iterate over all branches to see recent changes,
 # as the recent changes (Jan 28th) are all in the repo_mining branch!
 # TODO iterate over all branches
 # TODO get and return full file name, so that I can differentiate dir1/text.txt from dir2/text.txt
 # IN-PROGRESS store file names, assign unique file_id per repetitive file
 repo = githubInstance.get_repo("kennethken73/Group-4")

 print(repo.name)
 print(repo.description)

 contents = repo.get_contents("")
 while contents:
  file_content = contents.pop(0)
  if file_content.type == "dir":
   contents.extend(repo.get_contents(file_content.path))
  else:
   print(file_content)
 
 print('\n---------Commits----------')

 branch_list = repo.get_branches()
 commit_list = repo.get_commits()
 branch_count = branch_list.totalCount
 # print(commit_list) # returns PaginatedList
 
 commit_count = commit_list.totalCount
 print('Total number of commits:  ', commit_count, '\n')
 print('Total number of branches: ', branch_count, '\n')
 
 commit_record = []
 file_id = 0 # counter to index unique files. Two same-named files assigned the same id. Newly indexed per run of this function.
 commit_names = {} # k/v pair name->id. Untested for same-named files in different directories.
 for commit in commit_list:
  commit_author = commit.author.name
  commit_date = commit.commit.author.date
  week_n = commit_date.isocalendar().week # calendar week (week 1 includes Jan 1st)
  week_n -= 3 # Class begun on calendar.week == 4, so that week is group-4's first week. Subtract 3.
  day_n = commit_date.timetuple().tm_yday
  day_n -= 23 # First commit on Jan 24rd (24rd day of the year). This is repo's first day. Subtract 23.
  project_start_date = datetime(2025, 1, 21, 17, 00)
  # when in the project's lifetime (in hours) was the commit.
  hour_n = commit_date.replace(tzinfo=None) - project_start_date.replace(tzinfo=None)
  hour_n = hour_n.total_seconds() / 3600.0
  for file in commit.files:
   file_path = file.raw_url
   if file.filename not in commit_names:  # TODO dir1/th.tx vs dir2/th.tx
    file_id += 1
    commit_names[file.filename] = file_id

   commit_record.append({"file": file.filename,
                         "path": file_path,
                         "id": commit_names[file.filename],
                         # "url": file_path,
                         "contributor": commit_author,
                         "date": commit_date,
                         "week": week_n,
                         "day": day_n,
                         "hour": hour_n})
 
 return commit_record
#######################################################################################################
  

# function:printCommitRecord
#######################################################################################################
def printCommitRecord(commit_record):
 for c in commit_record:
  # print('\n-----------------------------------------------------------------------------------------')
  print(c.get("file"), ':\n'
        '   path: ', c.get("path"), '\n',
        '   id: ', c.get("id"), '\n',
        '   changed by ', c.get("contributor"), '\n',
        '   on date: ', c.get("date"), '\n',
        '   on week: ', c.get("week"), '\n',
        '   on project_day: ', c.get("day"), '\n',
        '   on project_hour: ', c.get("hour"))
  # print('-----------------------------------------------------------------------------------------\n')
#######################################################################################################

if __name__ == "__main__":
 printCommitRecord(getCommitRecord())


