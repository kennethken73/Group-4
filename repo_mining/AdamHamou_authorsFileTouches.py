import json
import requests
import csv
from datetime import datetime
import os

if not os.path.exists("data"):
    os.makedirs("data")

SOURCE = {".kt", ".java",  ".c",  ".cpp",  ".h",  ".xml",  ".gradle", ".kts", 
    ".sh",  ".mk"}     
     
# GitHub Authentication function
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

# Function to check if a file is a source file
def is_source_file(filename):
    return any(filename.endswith(ext) for ext in SOURCE)

# Collect author information and timestamps
def collect_authors_data(repo, lsttokens):
    authors_data = {}
    ipage = 1
    ct = 0

    try:
        while True:
            spage = str(ipage)
            commitsUrl = f'https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            if not jsonCommits or len(jsonCommits) == 0:
                break

            for shaObject in jsonCommits:
                sha = shaObject['sha']
                author = shaObject["commit"]["author"]["name"]
                date = shaObject["commit"]["author"]["date"]

                shaUrl = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)

                if "files" in shaDetails:
                    for fileObj in shaDetails["files"]:
                        filename = fileObj["filename"]

                        if is_source_file(filename):
                            if filename not in authors_data:
                                authors_data[filename] = []

                            authors_data[filename].append((author, date))

            ipage += 1

    except:
        print("Error receiving data")
        exit(0)

    return authors_data

# GitHub repo
repo = 'scottyab/rootbeer'

# put your tokens here
# Remember to empty the list when going to commit to GitHub.

# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = [""]

# Collect author data & save to csv
authors_data = collect_authors_data(repo, lstTokens)

fileOutput = f'data/authors_{repo.split("/")[1]}.csv'

with open(fileOutput, 'w', newline='') as fileCSV:
    writer = csv.writer(fileCSV)
    writer.writerow(["Filename", "Author", "Date"])

    for filename, touches in authors_data.items():
        for author, date in touches:
            writer.writerow([filename, author, date])

print(f"Data saved to {fileOutput}")