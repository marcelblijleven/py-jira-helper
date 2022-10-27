import dataclasses
import json
from datetime import datetime

import httpx


@dataclasses.dataclass
class FixVersion:
    url: str
    id: str
    name: str
    archived: bool
    released: bool
    releaseDate: bool


class Api:
    default_headers = {"Accept": "application/json", "Content-Type": "application/json"}

    def __init__(self, project: str, host: str, email: str, token: str):
        self.api_endpoint = "/rest/api/latest"
        self.project = project
        self.host = host
        self._email = email
        self._token = token

    def create_fix_version(self, version: str, released: bool = False, has_tickets: bool = True) -> None:
        endpoint = self.host + self.api_endpoint + "/version"

        body = {
            "name": version,
            "project": self.project,
            "released": released,
        }

        if released:
            body.update({"releaseDate": datetime.now().strftime("%Y-%m-%d")})

            if not has_tickets:
                body.update(
                    {
                        'description': 'This release does not contain any work that can be linked to tickets'
                    }
                )
        elif not released and not has_tickets:
            body.update(
                {
                    'description': 'This pre-release does not contain any work that can be linked to tickets'
                }
            )

        with httpx.Client(headers=self.default_headers) as client:
            client.auth = httpx.BasicAuth(username=self._email, password=self._token)
            response = client.post(url=endpoint, content=json.dumps(body))

        if int(response.status_code / 100) != 2:
            raise ValueError(response.read())

    def assign_version(self, issue: str, version: str):
        endpoint = self.host + self.api_endpoint + "/issue/" + issue

        body = {"update": {"fixVersions": [{"add": {"name": version}}]}}

        with httpx.Client(headers=self.default_headers) as client:
            client.auth = httpx.BasicAuth(username=self._email, password=self._token)
            response = client.put(url=endpoint, content=json.dumps(body))

        response.raise_for_status()

    def get_ticket_versions(self, issue: str) -> list[FixVersion]:
        endpoint = (
            self.host + self.api_endpoint + "/issue/" + issue + "?fields=fixVersions"
        )

        with httpx.Client(headers=self.default_headers) as client:
            client.auth = httpx.BasicAuth(username=self._email, password=self._token)
            response = client.get(url=endpoint)

        response.raise_for_status()

        data = response.json()

        if not (fields := data.get("fields")) or not (
            versions := fields.get("fixVersions")
        ):
            return []

        fix_versions = [
            FixVersion(
                url=version.get("self"),
                id=version.get("id"),
                name=version.get("name"),
                archived=version.get("archived"),
                released=version.get("released"),
                releaseDate=version.get("releaseDate"),
            )
            for version in versions
        ]

        return fix_versions
