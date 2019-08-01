import json
import requests

from .exceptions import ResourceNotFoundException, ErrorResponseException


class RedashAPIClient(object):
    def __init__(self, api_key, host):
        self.host = host
        self.api_key = api_key

        self.s = requests.Session()
        self.s.headers.update({'Authorization': f'Key {api_key}'})

    def create_query(self, name, data_source_name: str, query: str, description='', is_publish: bool = True):
        data_source = self.get_data_source_by_name(data_source_name)
        data_source_id = data_source['id']
        payload = {
            'name': name,
            'data_source_id': data_source_id,
            'query': query,
            'description': description,
        }
        res = self._post('queries', payload)

        if is_publish:
            self.update_query(
                query_id=res['id'],
                is_publish=is_publish,
            )
        return res

    def update_query(
            self,
            query_id: int,
            name=None,
            data_source_name: str = None,
            query: str = None,
            description: str = None,
            is_publish: bool = True
    ):
        payload = {}
        if name:
            payload['name'] = name
        if data_source_name:
            data_source = self.get_data_source_by_name(data_source_name)
            payload['data_source_id'] = data_source['id']
        if query:
            payload['query'] = query
        if description:
            payload['description'] = description
        # draft false is published
        payload['is_draft'] = not is_publish

        return self._post(f'queries/{query_id}', payload)

    def update_or_create_query(
            self,
            query_id: int,
            name=None,
            data_source_name: str = None,
            query: str = None,
            description: str = None,
            is_publish: bool = True
    ):
        pass

    def get_query_by_id(self, query_id):
        return self._get(f'queries/{query_id}')

    def get_data_sources(self):
        """
        [
            {
                "name": "hogehoge",
                "pause_reason": null,
                "syntax": "sql",
                "paused": 0,
                "view_only": false,
                "type": "pg",
                "id": 1
            },
            {
                "name": "fugafuga",
                "pause_reason": null,
                "syntax": "sql",
                "paused": 0,
                "view_only": false,
                "type": "athena",
                "id": 2
            },
        ]
        :return:
        """
        return self._get('data_sources')

    def get_data_source_by_name(self, name: str):
        """
        {
            "name": "hogehoge",
            "pause_reason": null,
            "syntax": "sql",
            "paused": 0,
            "view_only": false,
            "type": "pg",
            "id": 1
        },
        :param name:
        :return:
        """
        data_sources = self.get_data_sources()
        for data_source in data_sources:
            if data_source['name'] == name:
                return data_source
        raise ResourceNotFoundException(f'{name} is not found')

    def _get(self, uri):
        res = self.s.get(f'{self.host}/api/{uri}')

        if res.status_code != 200:
            raise ErrorResponseException(f'Retrieve data from URL: /api/{uri} failed.', status_code=res.status_code)

        return res.json()

    def _post(self, uri, payload=None):
        if not payload:
            data = json.dumps({})
        else:
            data = json.dumps(payload)

        self.s.headers.update({'Content-Type': 'application/json'})
        res = self.s.post(f'{self.host}/api/{uri}', data=data)

        if res.status_code != 200:
            raise ErrorResponseException(f'Post data to URL: /api/{uri} failed.', status_code=res.status_code)

        return res.json()

    def _delete(self, uri):
        res = self.s.delete(f'{self.host}/api/{uri}')

        if res.status_code != 200:
            raise ErrorResponseException(f'Delete data from URL: /api/{uri} failed.', status_code=res.status_code)

        return res.json()
