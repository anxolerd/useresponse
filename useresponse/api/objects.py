from enum import Enum
from typing import Dict
from typing import Optional


class ObjectOwnership(Enum):
    feedback = 'feedback'
    helpdesk = 'helpdesk'
    announcements = 'announcements'
    knowledge_base = 'knowledge-base'


class ObjectType(Enum):
    # Feedback object types
    problem = 'problem'
    thanks = 'thanks'
    question = 'question'
    idea = 'idea'

    # Helpdesk object types
    ticket = 'ticket'

    # Announcement object types
    announcement = 'announcement'

    # Knowledge-base object types
    article = 'article'
    faq = 'faq'


class ObjectService(object):
    """Service which contains objects-related API calls"""

    def __init__(self, transport):
        self._transport = transport

    def get(self, id_: int) -> Optional[Dict]:
        """Retrieves object by id

        :param id_: (int) id of the object to retrieve
        :return: Dict which represents existing object, if any, otherwise None
        """
        return self._transport.get(f'/objects/{id_}.json', {})

    def create(
        self,
        ownership: ObjectOwnership,
        object_type: ObjectType,
        title: str,
        content: str,
        **extended_parameters: dict,
    ) -> Optional[Dict]:
        """Create new object

        :param ownership: (ObjectOwnership) Object belongs to a logical group.
        :param object_type: (ObjectType) Type of object
        :param title: (str) The title of a new object.
        Max title length: 100 chars.
        :param content: (str) The content of a new object.
        Supports BBcode, but HTML tags are not allowed.
        Max content length: 12000 chars
        :return: Dict which represents existing object, if any, otherwise None
        """
        request_params = {
            **extended_parameters, **{
                'ownership': ownership,
                'object_type': object_type,
                'title': title,
                'content': content,
            }
        }
        result = self._transport.post('/objects.json', request_params)
        return result['success'] if result['success'] else None
