import sys
import json
import urllib.request
import urllib.error

def fetch_github_activity(username):
    """
    Fetches the recent public events for a given GitHub username.
    """
    url = f"https://api.github.com/users/{username}/events"
    
    headers = {"User-Agent": "Python-CLI-App"}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                raw_data = response.read().decode("utf-8")
                events = json.loads(raw_data)
                return events
                
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: User '{username}' not found.")
        elif e.code == 403:
            print("Error: API rate limit exceeded or access forbidden.")
        else:
            print(f"HTTP Error {e.code}: {e.reason}")
        sys.exit(1)
        
    except urllib.error.URLError as e:
        print(f"Network Error: Unable to reach the server ({e.reason}).")
        sys.exit(1)

def format_event(event):
    """
    Converts a single GitHub event dictionary into a clean string line.
    """
    event_type = event.get("type")
    repo_name = event.get("repo", {}).get("name", "unknown repository")
    payload = event.get("payload", {})
    
    if event_type == "PushEvent":
        commit_count = len(payload.get("commits", []))
        return f"- Pushed {commit_count} commit(s) to {repo_name}"
        
    elif event_type == "IssuesEvent":
        action = payload.get("action", "opened")
        return f"- {action.capitalize()} an issue in {repo_name}"
        
    elif event_type == "WatchEvent":
        return f"- Starred {repo_name}"
        
    elif event_type == "CreateEvent":
        ref_type = payload.get("ref_type", "repository")
        return f"- Created a {ref_type} in {repo_name}"
        
    elif event_type == "ForkEvent":
        return f"- Forked {repo_name}"
        
    elif event_type == "IssueCommentEvent":
        action = payload.get("action", "created")
        return f"- {action.capitalize()} a comment on an issue in {repo_name}"
        
    elif event_type == "PullRequestEvent":
        action = payload.get("action", "opened")
        return f"- {action.capitalize()} a pull request in {repo_name}"
        
    else:
    
        clean_name = event_type.replace("Event", "") if event_type else "Activity"
        return f"- Performed {clean_name} action in {repo_name}"

def main():
    
    if len(sys.argv) < 2:
        print("Usage: python github_activity.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    
    
    events = fetch_github_activity(username)
    
    
    if not events:
        print(f"No recent public activity found for user '{username}'.")
        return

    
    print("\nOutput:")
    for event in events[:10]:  
        print(format_event(event))

if __name__ == "__main__":
    main()