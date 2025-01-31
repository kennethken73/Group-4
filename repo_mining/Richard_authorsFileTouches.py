import json
import requests
import csv
import os
import time

if not os.path.exists("data"):
    os.makedirs("data")


# GitHub Authentication function with rate limit handling
def github_auth(url, lsttokens, ct):
    jsonData = None
    retries = 3
    while retries > 0:
        try:
            ct = ct % len(lsttokens)
            headers = {'Authorization': f'Bearer {lsttokens[ct]}'}
            response = requests.get(url, headers=headers)

            if response.status_code == 403: # rate limit exceeded
                print("Rate limit exceeded. Waiting 60 seconds before retrying...")
                time.sleep(60)
                retries -= 1
                continue

            response.raise_for_status()
            jsonData = json.loads(response.content)
            ct += 1
            return jsonData, ct
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            retries -= 1
            time.sleep(10)  # wait before retrying
    return None, ct


# collect authors and dates for source files
def collect_authors_and_dates(repo, lsttokens, source_extensions):
    file_data = {}
    all_authors = {}
    ipage = 1  # URL page counter
    ct = 0  # token counter

    try:
        while True:
            spage = str(ipage)
            commits_url = f'https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100'
            commits, ct = github_auth(commits_url, lsttokens, ct)

            if not commits or len(commits) == 0:  # no more commits to read
                break

            for commit in commits:
                sha = commit['sha']
                commit_url = f'https://api.github.com/repos/{repo}/commits/{sha}'
                commit_details, ct = github_auth(commit_url, lsttokens, ct)

                if commit_details is None:
                    continue  # skip if API request failed

                author = commit_details['commit']['author']['name']
                date = commit_details['commit']['author']['date']

                # track total contributions per author
                all_authors[author] = all_authors.get(author, 0) + 1

                # extract files touched in the commit
                for file in commit_details.get('files', []):
                    filename = file['filename']

                    # filter for source files by extension
                    if any(filename.endswith(ext) for ext in source_extensions):
                        if filename not in file_data:
                            file_data[filename] = []
                        file_data[filename].append((author, date))
                        print(f"File: {filename}, Author: {author}, Date: {date}")

            ipage += 1  # move to the next page of commits
    except Exception as e:
        print(f"Error during data collection: {e}")
        return None, None

    return file_data, all_authors


if __name__ == "__main__":

    repo = "scottyab/rootbeer"
    lstTokens = ["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"]

    source_extensions = ['.py', '.java', '.c', '.cpp', '.js', '.ts']

    file_authors_dates, all_authors = collect_authors_and_dates(repo, lstTokens, source_extensions)

    if file_authors_dates:
        # save authors and file modification data to CSV file
        output_file = f"data/authors_file_touches.csv"
        with open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Filename", "Author", "Date"])
            for filename, touches in file_authors_dates.items():
                for author, date in touches:
                    writer.writerow([filename, author, date])
        print(f"Data saved to {output_file}")

    if all_authors:
        # save total contributions per author
        author_output_file = f"data/authors_contributions.csv"
        with open(author_output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Author", "Commits"])
            for author, commits in sorted(all_authors.items(), key=lambda x: x[1], reverse=True):
                writer.writerow([author, commits])
        print(f"Author contributions saved to {author_output_file}")
