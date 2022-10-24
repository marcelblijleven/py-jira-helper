import re


def get_jira_tickets(data: str, prefix: str) -> list[str]:
    """
    Retrieves all jira ticket/issue numbers from the provided string
    :param data: string with commit messages
    :param prefix: jira issue prefix
    """
    raw_output = re.findall(rf'{prefix}-\d+', data)

    if not raw_output:
        return []

    checked_output = set()

    for value in raw_output:
        project, number = value.split('-')

        if project != 'JC' or not int(number):
            continue

        checked_output.add(value)

    return list(checked_output)


def is_prerelease(version: str) -> bool:
    """
    Checks if the version is a prerelease by matching it to exactly v<MAJOR>.<MINOR>.<PATCH>
    :param version: string containing the version (tag)
    """
    pattern = re.compile(r'^v[\d.]+$')
    return bool(pattern.match(version))
