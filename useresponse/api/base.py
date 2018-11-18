from typing import Any, Dict

import requests

from .users import UserService


class API(object):
    def __init__(self, useresponse_domain: str, api_token: str) -> None:
        self._transport  = _Transport(useresponse_domain, api_token)

        # register services
        self.users = UserService(self._transport)

    def __setattr__(self, name: str, value: Any) -> None:
        protected_attrs = ('users',)
        if name in protected_attrs and hasattr(self, name):
            raise ValueError(f'Cannot modify attribute {name}')
        super(API, self).__setattr__(name, value)


class _Transport(object):
    def __init__(self, domain: str, api_token: str) -> None:
        self._domain = domain
        self._api_token = api_token

    def _get_url(self, path: str) -> str:
        return f'{self._domain}/api/4.0{path}'

    def get(self, path: str, params: Dict[str, Any]) -> requests.Response:
        params = dict(params, **{'apiKey': self._api_token})
        response = requests.get(self._get_url(path), params=params)
        return response

    def post(self, path: str, body: Dict[str, Any]) -> requests.Response:
        body = dict(body, **{'apiKey': self._api_token})
        pass

    def put(self, path: str, body: Dict[str, Any]) -> requests.Response:
        body = dict(body, **{'apiKey': self._api_token})
        pass

    def delete(self, path: str) -> requests.Response:
        params = {'apiKey': self._api_token}
        pass
