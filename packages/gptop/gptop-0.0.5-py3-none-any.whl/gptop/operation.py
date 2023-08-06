import json as _json
import requests as _requests
from enum import Enum as _Enum


class OperationType(str, _Enum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class Operation():

    def __init__(self, id: str, type: OperationType, name: str, description: str,
                 url: str, path: str, requires_auth: bool, schema: any):
        """
        Holds the properties on an operation prepared for execution
        - id: The identifier of the operation
        - type: The type of operation
        - name: The name of the operation
        - description: The description of the operation
        - url: The url of the operation
        - path: The path to the operation
        - requires_auth: If the operation requires authentication
        - schema: The schema of the operation
        """

        self.id = id
        self.type = type
        self.name = name
        self.description = description
        self.url = url
        self.path = path
        self.requires_auth = requires_auth
        self.schema = schema

    def __repr__(self) -> str:
        return _json.dumps(self.__dict__)

    @classmethod
    def from_obj(self, obj):
        """
        Returns an instance of an operation from a dict object
        """

        return Operation(obj['id'], obj['type'], obj['name'], obj['description'],
                         obj['url'], obj['path'], obj['auth'], obj['schema'])

    def metadata(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "url": self.url,
            "path": self.path,
            "auth": self.requires_auth,
            "schema": self.schema
        }

    def embedding_obj(self):
        return "; ".join([
            f"Name: {self.name}",
            f"Description: {self.description}",
            f"Type: {self.type}",
            f"URL: {self.url}",
            f"Path: {self.path}",
            f"Requires Auth: {self.requires_auth}",
            f"Schema: {self.schema}"
        ])

    def endpoint(self) -> str:
        return self.url + self.path

    def execute(self, params, body, auth_token=None):
        """
        Executes the command.

        Returns: The response provided by the execution API
        """

        result = None
        data = _json.dumps(body).encode('utf-8')

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        if self.requires_auth:
            headers["Authorization"] = f"Bearer {auth_token}"

        if self.type == OperationType.POST:
            result = _requests.post(
                self.endpoint(),
                headers=headers,
                params=params,
                data=data
            )

        elif self.type == OperationType.GET:
            result = _requests.get(
                self.endpoint(),
                headers=headers,
                params=params,
                data=data
            )

        elif self.type == OperationType.PUT:
            result = _requests.put(
                self.endpoint(),
                headers=headers,
                params=params,
                data=data
            )

        elif self.type == OperationType.PATCH:
            result = _requests.patch(
                self.endpoint(),
                headers=headers,
                params=params,
                data=data
            )

        elif self.type == OperationType.DELETE:
            result = _requests.delete(
                self.endpoint(),
                headers=headers,
                params=params,
                data=data
            )

        if not result:
            return None

        return result.json()
