import json
import requests
import csv
import os
from datetime import datetime

if not os.path.exists("data"):
    os.makedirs("data")

lstTokens = [""]
repo = 'scottyab/rootbeer'
source_file_extensions = {
    ".java", ".kt", ".c", ".cpp", ".h", ".gradle",
    ".groovy", ".m", ".mm", ".swift", ".py"
}
    
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lsttoken)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        response = requests.get(url, headers=headers)
        jsonData = response.json()
        ct += 1
    except Exception as e:
        print(e)
    return jsonData, ct

def get_file_commit(dict_info, tokens, repo):
    page = 1
    index = 0
    while True:
        commits_url = f"https://api.github.com/repos/{repo}/commits?page={page}&per_page=100"
        commits_json, index = github_auth(commits_url, tokens, index)

        if len(commits_json) == 0:
            break

        for commit_obj in commits_json:
            sha = commit_obj.get("sha")
            if not sha:
                continue
            sha_url = f"https://api.github.com/repos/{repo}/commits/{sha}"
            sha_details, index = github_auth(sha_url, tokens, index)
            if not sha_details:
                continue

            commit_author = sha_details.get("commit", {}).get("author", {}).get("name", "UnknownAuthor")
            commit_date = sha_details.get("commit", {}).get("author", {}).get("date", "UnknownDate")

            files_list = sha_details.get("files", [])
            for f in files_list:
                filename = f.get("filename", "")
                _, file_extension = os.path.splitext(filename)
                if file_extension.lower() in source_file_extensions:
                    if filename not in dict_info:
                        dict_info[filename] = []
                    dict_info[filename].append({
                        "author": commit_author,
                        "date": commit_date
                    })

        page += 1

def main():
    dict_file_authors = {}
    get_file_commit(dict_file_authors, lstTokens, repo)

    for filename, commit_list in dict_file_authors.items():
        for commit_info in commit_list:
            print(f"Filename: {filename} | Author: {commit_info['author']} | Date: {commit_info['date']}")

    csv_file_path = os.path.join("data", "commit_data.csv")
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Filename", "Author", "Date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for filename, commit_list in dict_file_authors.items():
            for commit_info in commit_list:
                writer.writerow({
                    "Filename": filename,
                    "Author": commit_info["author"],
                    "Date": commit_info["date"]
                })

if __name__ == "__main__":
    main()
