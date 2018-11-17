from hashlib import md5, sha1
from typing import Dict, Optional, Union
from urllib.parse import urlencode


__all__ = (
    'UseresponseSso',
)


def to_base(number: int, base: int) -> str:
    """Produces representation of givent number in base

    Implementation borrowed from here: https://bit.ly/2OrlJlH
    """
    digits = '0123456789abcdefghijklmnopqrstuvwxyz'
    if base > len(digits):
        raise ValueError("Bases greater than 36 not handled in base_repr.")
    elif base < 2:
        raise ValueError("Bases less than 2 not handled in base_repr.")

    num = abs(number)
    res = []
    while num:
        res.append(digits[num % base])
        num //= base
    if number < 0:
        res.append('-')
    return ''.join(reversed(res or '0'))


class UseresponseSso(object):
    """ Helper class for Useresponse Single-Sign-On

    Ref: https://help.useresponse.com/knowledge-base/article/single-sign-on

    Usage:
        >>> useresponse = UseresponseSso(
        ...     domain='https://useresponse.domain',
        ...     secret='s3kre7',
        ...     source='example.com',
        ...     full_name='John Doe',
        ...     email='johndoe@example.com',
        ...     user_id=42,
        ... )
        >>> login_url = useresponse.get_login_url()
        >>> redirect(login_url)

    Useresponce recently added custom fields support in their API. Those are
    supported via optional ``properties`` param. Here is how to use it:

        >>> useresponse = UseresponseSso(
        ...    ...
        ...    properties={
        ...        172: 'lorem ipsum',
        ...        198: '2018-01-01',
        ...    },
        ... )

    Here the key is the custom fields's id, which can be taken from
    Administration » Fields & Properties » Users, and the value is the custom
    field's value

    P.S. sorry for shitty cryptography =( I wish there was normal crypto here
    """
    def __init__(
        self,
        domain: str,
        secret: str,
        source: str,
        full_name: str,
        email: str,
        user_id: Union[int, str],
        properties: Optional[Dict[int, str]]=None,
    ):
        if properties is None:
            properties = {}
        self.domain: str = domain
        self.secret: str = secret
        self.full_name: str = full_name
        self.email: str = email
        self.user_id: str = str(user_id)
        self.source = source
        self.properties = properties

    def get_login_url(self, redirect_url: Optional[str] = None) -> str:
        """Returns useresponse login url

        If ``redirect_url`` param is provided, this method generates url which
        should redirect user to ``redirect_url`` after success
        """
        url = self._get_base_login_url()
        query_params = {}
        if redirect_url is not None:
            query_params.update({'redirect': redirect_url})
        if self.properties:
            query_params.update(self._prepare_properties_params())
        url += ('?' + urlencode(query_params))
        return url

    def _prepare_properties_params(self) -> Dict[str, str]:
        def _key(property_id: int) -> str:
            return f'properties[property_{property_id}]'

        return {
            _key(property_id): self._encrypt(property_value)
            for (property_id, property_value) in self.properties.items()
        }

    def _get_base_login_url(self) -> str:
        parts = (
            self.domain,
            'sso',
            self._encrypt(self.source),
            self._encrypt(self.full_name),
            self._encrypt(self.email),
            self._encrypt(self.user_id),
            self._generate_hash(),
            'direct-sso',
        )
        return '/'.join(parts)

    def _encrypt(self, string: str) -> str:
        key: str = sha1(self.secret.encode('utf-8')).hexdigest()
        str_bytes: bytes = string.encode('utf-8')

        hashed: str = ''
        for i in range(len(str_bytes)):
            ord_str = str_bytes[i]
            ord_key = ord(key[i % len(key)])
            hashed += to_base(ord_str + ord_key, 36)[::-1]
        return hashed

    def _generate_hash(self) -> str:
        key = sha1(
            md5(self.secret.encode('utf-8')[::-1])
            .hexdigest()
            .encode('utf-8')
        ).hexdigest()
        hashable = key.join([
            self.full_name,
            self.user_id,
            self.email,
            self.source,
        ])
        return sha1(hashable.encode('utf-8')[::-1]).hexdigest()
