from collections import defaultdict
import json
import csv
import os
import sys
import requests

if not os.path.exists("data"):
    os.makedirs("data")

#GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': f'Bearer {lsttoken[ct]}'}
        request = requests.get(url, headers=headers, timeout=10)
        jsonData = json.loads(request.content)
        ct += 1
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error: {e}")
    return jsonData, ct

#function to get the filenames, authors, and dates of files in a repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1   # url page counter
    ct = 0      # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            #break the loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            
            #iterate through the list of commits in spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                author = shaObject['commit']['author']['name']
                date = shaObject['commit']['author']['date']

                #for each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']

                # iterate through the list of files in filesjson and if the file is a source file, add it to the dictionary
                for filenameObj in filesjson:
                    filename = filenameObj['filename']

                    #check if the file is a source file, if it is, add it to the dictionary along with the author and date
                    if filename.endswith('.java') or filename.endswith('.kt') or filename.endswith('.cpp') or filename.endswith('.h'):
                        dictfiles[filename]["authors"].append(author)
                        dictfiles[filename]["dates"].append(date)
                        dictfiles[filename]["touch_count"] += 1
                        print(filename)
            ipage += 1
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error receiving data: {e}")
        sys.exit(1)

# GitHub repo
repo = 'scottyab/rootbeer'

# GitHub authentication tokens
lstTokens = ["removed for security"]

# dictionary to store data for final file authors CSV 
dictfiles = defaultdict(lambda: {"authors": [], "dates": [], "touch_count": 0})
countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

#extract the file name from repo
file = repo.split('/')[1]

# Define the output file path
fileOutput = os.path.join('data', f'file_{file}_authors.csv')

#Define the header row
header = ["Filename", "Authors", "Dates", "Touch Count"]

#write to the CSV file
with open(fileOutput, 'w', encoding='utf-8', newline='') as fileCSV:
    writer = csv.writer(fileCSV)
    writer.writerow(header)  # Write the header row

    # Iterate through the data and write rows
    for filename, details in dictfiles.items():
        authors = ', '.join(details['authors'])  # Convert authors list to a comma-separated string
        dates = ', '.join(details['dates'])      # Convert dates list to a comma-separated string
        touch_count = details['touch_count']     # get touch count
        writer.writerow([filename, authors, dates, touch_count])

print(f'{fileOutput} has been created')
