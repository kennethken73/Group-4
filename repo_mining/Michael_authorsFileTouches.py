import json
import requests
import csv
import os

# source file extensions
source_extensions = ['.py', '.java', '.js', '.cpp', '.h', '.rb', '.go']

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lsttoken)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print(e)
    return jsonData, ct

# Function to collect authors and timestamps for each source file
def collect_authors_timestamps(dictfiles, lsttokens, repo):
    ipage = 1  # Page counter for pagination
    ct = 0  # Token counter

    try:
        while True:
            spage = str(ipage)
            commits_url = f'https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100'
            jsonCommits, ct = github_auth(commits_url, lsttokens, ct)

            if len(jsonCommits) == 0:
                break  # when no more commits

            for commit in jsonCommits:
                sha = commit['sha']
                author = commit['commit']['author']['name']
                date = commit['commit']['author']['date']

                # Get details of files modified in this commit
                sha_url = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, ct = github_auth(sha_url, lsttokens, ct)
                filesjson = shaDetails.get('files', [])

                for file_obj in filesjson:
                    filename = file_obj['filename']

                    # Only include source files
                    if any(filename.endswith(ext) for ext in source_extensions):
                        if filename not in dictfiles:
                            dictfiles[filename] = []
                        dictfiles[filename].append((author, date))

            ipage += 1

    except Exception as e:
        print("Error fetching data:", e)
        exit(0)

# GitHub repo 
repo = 'scottyab/rootbeer'

# GitHub token
lstTokens = [""]

# Dictionary to store file authors and timestamps
dictfiles = dict()
collect_authors_timestamps(dictfiles, lstTokens, repo)

# Save results to CSV
if not os.path.exists("data"):
    os.makedirs("data")

fileOutput = f"data/authors_{repo.split('/')[1]}.csv"
with open(fileOutput, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Filename", "Author", "Date"])

    for filename, touches in dictfiles.items():
        for author, date in touches:
            writer.writerow([filename, author, date])

print(f"Data saved to {fileOutput}")
