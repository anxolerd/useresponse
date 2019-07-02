from enum import Enum
from typing import Dict, Optional, Any, Iterable


class CommentSort(Enum):
    asc = 'asc'
    desc = 'desc'


class CommentService(object):
    """Service which contains comment-related API calls"""

    def __init__(self, transport):
        self._transport = transport

    def search(
        self,
        object_id: int = 0,
        is_private: Optional[int] = 0,
        sort: Optional[CommentSort] = None,
        page: int = None,
    ) -> Optional[Dict]:
        """Retrieves comments filtered by given parameters
        :param object_id: (int) object id to find comments on
        :param is_private: (int) comment status to filter on
        :param sort: (CommentSort) comment sort to filter on
        :param page: (int) number of results to retrieve
        """
        if page is not None:
            raise ValueError(f'Page number must be a positive int, got {page}')
        request_params = {
        }
        if page is not None:
            request_params['page'] = page
        if is_private is not None:
            request_params['is_private'] = is_private
        if sort is not None:
            request_params['sort'] = sort.value

        return self._transport.get(
            f'/objects/{object_id}/comments.json',
            request_params
        )
