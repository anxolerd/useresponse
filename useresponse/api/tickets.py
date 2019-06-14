from enum import Enum
from typing import Dict, Optional, Any, Iterable


class TicketStatus(Enum):
    all = 'all'
    opened = 'opened'
    on_hold = 'on_hold'
    in_progress = 'in_progress'
    awaiting_reply = 'awaiting_reply'
    all_active = 'all-active'
    completed = 'completed'


class TicketDate(Enum):
    today = 'today'
    yesterday = 'yesterday'
    this_week = 'this_week'
    last_week = 'last_week'
    this_month = 'this_month'
    last_month = 'last_month'


class TicketSort(Enum):
    new = 'new'
    updated = 'updated'
    new_updated = 'new_updated'


class TicketService(object):
    """Service which contains tickets-related API calls"""

    def __init__(self, transport):
        self._transport = transport

    def search(
        self,
        text: Optional[str] = None,
        status: Optional[TicketStatus] = None,
        date: Optional[TicketDate] = None,
        author_id: Optional[int] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        sort: Optional[TicketSort] = None,
        page: int = 1,
        count: int = 20,
    ) -> Optional[Dict]:
        """Retrieves tickets filtered by given parameters
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
            request_params['status'] = status.value
        if date is not None:
            request_params['date'] = date.value
        if author_id is not None:
            request_params['author_id'] = author_id
        if custom_fields is not None:
            request_params['custom_fields'] = custom_fields
        if sort is not None:
            request_params['sort'] = sort.value

        return self._transport.get('/tickets.json', request_params)

    def search_iter(
        self,
        text: Optional[str] = None,
        status: Optional[TicketStatus] = None,
        date: Optional[TicketDate] = None,
        author_id: Optional[int] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        sort: Optional[TicketSort] = None,
    ) -> Iterable[Dict]:
        """Retrieves tickets filtered by given parameters

        Comparing this to :meth:`useresponse.api.tickets.TicketService.search`
        this method is on the higher level of abstraction.
        User do not have to care about pages and count_per_page, and just
        to iterate through results

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
        page: int = 1
        while True:
            results = self.search(
                text,
                status,
                date,
                author_id,
                custom_fields,
                sort,
                page=page,
            )
            total_pages = results['success']['totalPages']
            page += 1
            for value in results['success']['data']:
                yield value
            if page > total_pages:
                break
