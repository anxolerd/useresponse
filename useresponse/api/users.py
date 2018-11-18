class UserService(object):
    def __init__(self, transport):
        self._transport = transport

    def get(self, id_: int) -> dict:
        return self._transport.get(f'/users/{id_}.json', {})
