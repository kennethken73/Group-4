##################################################################
# Author:       John Zaleschuk                                   #
# Date:         1/29/2025                                        #
# Program:      John_authorsFileTouches.py                       #
# Description:  Declares launch arguements with launch.actions   #
#               Then starts the two required nodes, also         #
#               declaring parameters for talker                  #
##################################################################

import json
import requests
import csv
import os

# if the data directory doesnt exist, create it
if not os.path.exists("data"):
 os.makedirs("data")

# GitHub Authentication function
# unchanged from provided code
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# function for scraping the information, slightly modified from provided code
def get_commit_data(lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    
    # where the info is stored
    commit_data = []
    
    # list of source file extensions, could be updated to support more source file types
    source_file_extensions = [".py", ".java", ".cpp", ".c", ".cs", ".js", ".h"]

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            # parses commit pages, storing in jsonCommits
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            
            # iterate through the list of commits in page
            # shaObject isolates an individual commit
            # 'for each commit in commit page'
            for shaObject in jsonCommits:
                # sets the commit specific sha id
                sha = shaObject['sha']
                # adds the sha id, along with repo name into api URL to get an individual commit for scraping
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                # puts the commit info into shaDetails
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                
                # in the api commit layout, the name and date is found under commit -> author -> name/date
                # scrape the wanted information into variables
                author = shaDetails['commit']['author']['name']
                date = shaDetails['commit']['author']['date']
                
                # commits can contain multiple files, so we capture the 'files' section in the commit API into filejson
                filesjson = shaDetails['files']
                
                # 'for each file in the list of files in the commit'
                for filenameObj in filesjson:
                    # get the individual filename
                    filename = filenameObj['filename']
                    
                    #compares file extensions to our list of source files
                    if any(filename.endswith(extension) for extension in source_file_extensions):
                        # append with the author and date of the commit
                        commit_data.append([filename, author, date])
                    
            # page iterator         
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
        
    # return data so the function call looks nice   
    return commit_data


# GitHub repo for scraping
repo = 'scottyab/rootbeer'
# generated api token(s) go here
lstTokens = ["XXXX"]

# call the function, collect the data
commit_data = get_commit_data(lstTokens, repo)

# separates the repo name from the repo owner
file = repo.split('/')[1]
# sets filename to be written to
fileOutput = 'data/file_' + file + '.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for data in commit_data:
    writer.writerow(data)
    
print(f"Commit info on {len(commit_data)} source files from github.com/{repo} has been written to {fileOutput}")