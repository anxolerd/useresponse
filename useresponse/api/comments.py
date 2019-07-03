from enum import Enum
from typing import Dict, Optional, Any, Iterable


class CommentSort(Enum):
    asc = 'asc'
    desc = 'desc'


class CommentService(object):
    """Service which contains comment-related API calls"""

    def search_by_object_id(
        self,
        object_id: int = 0,
        is_private: bool = False,
        sort: Optional[CommentSort] = None,
        page: int = None,
    ) -> Optional[Dict]:
        """Retrieves comments filtered by given parameters
        :param object_id: (int) object id to find comments on
        :param is_private: (int) comment status to filter on
        :param sort: (CommentSort) comment sort to filter on
        :param page: (int) page to retrieve. With this option set useresponse
        will return selected page with limited number of comments. Only
        useresepsone knows how big is this number
        """
        request_params = {'is_private': int(is_private)}
        if page is not None:
            request_params['page'] = page
        if sort is not None:
            request_params['sort'] = sort.value

        return self._transport.get(
            f'/objects/{object_id}/comments.json',
            request_params
        )

    def __init__(self, transport):
        self._transport = transport
