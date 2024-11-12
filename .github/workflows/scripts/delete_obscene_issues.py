import requests
import json

def delete_issue(issue_number, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    headers = {"Authorization": f"token {token}"}
    response = requests.delete(url, headers=headers)
    response.raise_for_status()

def block_user(username, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/collaborators/{username}"
    headers = {"Authorization": f"token {token}"}
    response = requests.delete(url, headers=headers)
    response.raise_for_status()

def main(token):
    # Replace 'your_username' and 'your_repo' with your actual repository details
    owner = "your_username"
    repo = "your_repo"

    # Get all open issues
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=open"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    issues = json.loads(response.text)

    # Iterate through each issue and check for obscene content
    for issue in issues:
        title = issue['title']
        body = issue['body']
        if "obscene" in title or "obscene" in body or "abusive" in title or "abusive" in body or "porn" in title or "porn" in body:
            issue_number = issue['number']
            username = issue['user']['login']
            delete_issue(issue_number, token)
            block_user(username, token)
            print(f"Deleted issue #{issue_number} and blocked user {username}")

if __name__ == "__main__":
    token = os.environ['GITHUB_TOKEN']
    main(token)