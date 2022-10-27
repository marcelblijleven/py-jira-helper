import sys
from sys import stdout
from typing import Optional

import httpx

from pyreleaser.git import get_commits_between_tags, get_current_tag, get_previous_tag
from pyreleaser.jira import get_jira_tickets, Api
from pyreleaser.util.env import read_env_var
from pyreleaser.util.system import path_exists
from pyreleaser.util.types import PathType


def get_information_from_git(cwd: Optional[PathType] = None):
    current = get_current_tag(cwd)
    previous = get_previous_tag(current, cwd)
    commits_between_tags = get_commits_between_tags(previous, current, cwd)

    stdout.write(f'INFO: comparing tags {previous}^...{current}\n')
    stdout.write(f'INFO: found {len(commits_between_tags.splitlines())}')

    for commit in commits_between_tags.splitlines():
        stdout.write(f' - {commit}\n')

    return current, previous, commits_between_tags


def create_and_assign_jira_release(version: str, tickets: list[str]) -> None:
    jira_api = Api(
        host=read_env_var('RELEASER_HOST'),
        project=read_env_var('RELEASER_PROJECT'),
        email=read_env_var('RELEASER_EMAIL'),
        token=read_env_var('RELEASER_API_TOKEN'),
    )

    is_released = 'dev' not in version and 'staging' not in version

    try:
        jira_api.create_fix_version(version, is_released, has_tickets=bool(len(tickets)))
    except httpx.HTTPError as exc:
        sys.stderr.write(f'Error occurred while creating release: {exc}\n')
        sys.exit(1)


if __name__ == '__main__':
    try:
        if not path_exists((directory := sys.argv[1])):
            raise ValueError(f'ERROR: {directory} does not exist')
    except IndexError:
        directory = None

    current_tag, previous_tag, commits = get_information_from_git(directory)
    jira_tickets = get_jira_tickets(commits, read_env_var('ISSUE_PREFIX'))

    if jira_tickets:
        stdout.write('INFO: Found the following Jira tickets:\n')
        stdout.write('\n'.join([f'- {ticket}' for ticket in jira_tickets]) + '\n')
    else:
        stdout.write('INFO: No Jira tickets found in any of the commits\n')

    create_and_assign_jira_release(current_tag, jira_tickets)
