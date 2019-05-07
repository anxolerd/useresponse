from enum import Enum
from typing import Dict, Optional, Any


class TicketStatus(Enum):
    all = 0
    opened = 1
    on_hold = 2
    in_progress = 3
    awaiting_reply = 4
    completed = 5


class TicketDate(Enum):
    today = 0
    yesterday = 1
    this_week = 2
    last_week = 3
    this_month = 4
    last_month = 5


class TicketSort(Enum):
    new = 0
    updated = 1
    new_updated = 2


class TicketsService(object):
    """Service which contains tickets-related API calls"""

    def __init__(self, transport):
        self._transport = transport

    def get(self,
            text: str = None,
            status: Optional[TicketStatus] = None,
            date: Optional[TicketDate] = None,
            author_id: int = None,
            custom_fields: Dict[str, Any] = None,
            sort: Optional[TicketSort] = None,
            page: int = 1,
            count: int = 20,
            ) -> Optional[Dict]:
        """Retrieves tickets
        :param text: (str) ticket text to filter on
        :param status: (TicketStatus) ticket status to filter on
        :param date: (TicketDate) ticket date to filter on
        :param author_id: (int) ticket author id to filter on
        :param custom_fields: (dict) ticket custom field to filter on
        :param sort: (TicketSort) ticket sort to filter on
        :param page: (int) number of page of results to retrieve. Parameter is
        not present in useresponse api (hacked)
        :param count: (int) number of results per page
        """
        if page < 1:
            raise ValueError(f'Page number must be a positive int, got {page}')
        if count < 1 or count > 50:
            raise ValueError(f'Count must be between 1 and 50, got {count}')
        request_params = {
            'page': page,
            'count': count,
        }

        if text is not None:
            request_params['text'] = text
        if status is not None:
            request_params['status'] = status
        if date is not None:
            request_params['date'] = date
        if author_id is not None:
            request_params['author_id'] = author_id
        if custom_fields is not None:
            request_params['custom_fields'] = custom_fields
        if sort is not None:
            request_params['sort'] = sort

        return self._transport.get('/tickets.json', request_params)
