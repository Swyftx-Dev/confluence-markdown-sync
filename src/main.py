from os import environ, walk
from os.path import join, relpath
from typing import Dict

import requests
from dotenv import load_dotenv
from markdown import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension

load_dotenv()

workspace = environ.get('GITHUB_WORKSPACE')
if not workspace:
    print('No workspace is set')
    exit(1)

envs: Dict[str, str] = {}
for key in ['from', 'to', 'cloud', 'user', 'token']:
    value = environ.get(f'INPUT_{key.upper()}')
    if not value:
        print(f'Missing value for {key}')
        exit(1)
    envs[key] = value

root_page_id = envs['to']

# Function to create child page
def create_page(title, parent_id, content_html):
    url = f"https://{envs['cloud']}.atlassian.net/wiki/rest/api/content/"
    data = {
        "type": "page",
        "title": title,
        "ancestors": [{"id": parent_id}],
        "space": {"key": "SPACEKEY"},  # Replace with your space key
        "body": {
            "storage": {
                "value": content_html,
                "representation": "storage"
            }
        }
    }
    response = requests.post(url, json=data, auth=(envs['user'], envs['token']))
    return response.json()['id']

# Traverse the folder and sync each markdown file
for dirpath, _, filenames in walk(join(workspace, envs['from'])):
    parent_page_id = root_page_id

    # Create child pages for subfolders
    if dirpath != workspace:
        subfolder_name = relpath(dirpath, workspace)
        parent_page_id = create_page(subfolder_name, root_page_id, "Folder content")

    # Sync each markdown file as a new Confluence page
    for filename in filenames:
        if filename.endswith(".md"):
            with open(join(dirpath, filename), 'r') as f:
                md_content = f.read()
            html_content = markdown(md_content, extensions=[GithubFlavoredMarkdownExtension()])
            create_page(filename.replace(".md", ""), parent_page_id, html_content)

print(f'Successfully synced folder content to Confluence.')
