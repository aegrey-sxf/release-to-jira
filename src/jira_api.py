import os
import datetime
import requests
from requests.auth import HTTPBasicAuth

BASE = os.environ["INPUT_JIRA_SERVER"]
PROJECT = os.environ["INPUT_JIRA_PROJECT"]
USER = os.environ["INPUT_JIRA_USER"]
TOKEN = os.environ["INPUT_JIRA_TOKEN"]

base_url = f"{BASE}/rest/api/3/"
project_path = f"project/{PROJECT}"
auth = HTTPBasicAuth(USER, TOKEN)


def get(endpoint, params=None):
    return requests.get(
        base_url + project_path + "/" + endpoint, params=params, auth=auth
    ).json()


def post(endpoint, body):
    return requests.post(base_url + endpoint, json=body, auth=auth)


def put(endpoint, body):
    return requests.put(base_url + endpoint, json=body, auth=auth)


def get_project_id():
    return get("")["id"]


def get_or_create_release(release_name):
    result = get("version", {"query": release_name})
    now = datetime.datetime.now()
    formatted_date = now.strftime('%Y-%m-%d')
    if result["total"] == 0:  
        return post(
            "version",
            {"name": release_name, "projectId": get_project_id(), "releaseDate": formatted_date, "released": "true"},
        ).json()
    elif result["total"] > 1:
        raise Exception("Found multiple releases with the same name.")
    else:
        return result["values"][0]


def add_release_to_issue(release_name, issue):
    response = put(
        f"issue/{issue}",
        {"update": {"fixVersions": [{"add": {"name": release_name}}]}},
    )
    response.raise_for_status()
    return response.status_code == 204
