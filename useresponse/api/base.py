import http.client as httplib
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .users import UserService
from .tickets import TicketService
from .objects import ObjectService
from .exceptions import (
    InvalidRequestException,
    UnauthenticatedException,
    UnauthorizedException,
    OperationConflictException,
    InternalServerError,
    ServiceUnavailableError,
)


ERROR_STATUSES = {
    httplib.BAD_REQUEST: InvalidRequestException,
    httplib.UNAUTHORIZED: UnauthenticatedException,
    httplib.FORBIDDEN: UnauthorizedException,
    httplib.CONFLICT: OperationConflictException,
    httplib.INTERNAL_SERVER_ERROR: InternalServerError,
    httplib.SERVICE_UNAVAILABLE: ServiceUnavailableError,
}


class API(object):
    def __init__(self, useresponse_domain: str, api_token: str) -> None:
        self._transport = _Transport(useresponse_domain, api_token)

        # register services
        self.users: UserService = UserService(self._transport)
        self.tickets: TicketService = TicketService(self._transport)
        self.objects: ObjectService = ObjectService(self._transport)

    def __setattr__(self, name: str, value: Any) -> None:
        protected_attrs = ('users', 'tickets', 'objects',)
        if name in protected_attrs and hasattr(self, name):
            raise ValueError(f'Cannot modify attribute {name}')
        super(API, self).__setattr__(name, value)


class _Transport(object):
    def __init__(self, domain: str, api_token: str) -> None:
        self._domain = domain
        self._api_base = urljoin(self._domain, '/api/4.0/')
        self._api_token = api_token

    def get(self, path: str, params: Dict[str, Any]) -> Optional[Dict]:
        params = dict(params, **{'apiKey': self._api_token})
        response = requests.get(self._get_url(path), params=params)
        return self._process_response(response)

    def post(self, path: str, body: Dict[str, Any]) -> Optional[Dict]:
        body = dict(body, **{'apiKey': self._api_token})
        response = requests.post(self._get_url(path), data=body)
        return self._process_response(response)

    def put(self, path: str, body: Dict[str, Any]) -> Optional[Dict]:
        body = dict(body, **{'apiKey': self._api_token})
        response = requests.put(self._get_url(path), data=body)
        return self._process_response(response)

    def delete(self, path: str) -> Optional[Dict]:
        params = {'apiKey': self._api_token}
        response = requests.delete(self._get_url(path), params=params)
        return self._process_response(response)

    def _get_url(self, path: str) -> str:
        path = path.lstrip('/')
        return urljoin(self._api_base, path)

    def _process_response(self, response: requests.Response) -> Optional[Dict]:
        if response.status_code in ERROR_STATUSES:
            raise ERROR_STATUSES[response.status_code](response)
        if response.status_code == httplib.NO_CONTENT:
            return None
        return response.json()
