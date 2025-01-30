# Modified version of CollectFiles.py for getting author/date data
import json
import requests
import csv

import os
import numpy as np

# GitHub Authentication function - no reason to change this
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


# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # jsonCommits contains author names and dates for multiple commits
            # print("jsonCommits:\njsonCommits")

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)

                # shaDetails contains info on a commit: author, data, files touched
                # print("shaDetails:\nshaDetails")
                # break

                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']

                    # Get source files by checking extensions
                    # Source files are determined by the file extension
                    _, extension = os.path.splitext(filename)
                    if extension not in extensions:
                        continue

                    # Get author and date data
                    authorData = shaDetails['commit']['author']

                    # Add info to dictfiles
                    currentData = {filename: authorData['date']}
                    dictfiles[authorData['name']] = dictfiles.get(authorData['name'], [])
                    dictfiles[authorData['name']].append(currentData)

                    print(authorData['name'])
                    print(dictfiles[authorData['name']])
                    print()
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
# GitHub repo
repo = 'scottyab/rootbeer'

# Remember to delete token
lstTokens = []
                #"fd02a694b606c4120b8ca7bbe7ce29229376ee",
                #"16ce529bdb32263fb90a392d38b5f53c7ecb6b",
                #"8cea5715051869e98044f38b60fe897b350d4a"]

# Used for finding source codes; bit of a hard-coded solution though
extensions = ['.java', '.kts', '.kt', '.cpp', '.h', '.txt']

dictfiles = dict()  # Contains commit history (author/date) for each file
countfiles(dictfiles, lstTokens, repo)
# print('Total number of source files: ' + str(len(dictfiles)))

# Creating a file containing dictfiles to use for scatterplot.py
with open('Jayson_scatterplotData.txt', 'w') as file:
    json.dump(dictfiles, file)
