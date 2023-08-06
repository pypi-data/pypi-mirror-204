"""
Comments Class
"""
# Standard library modules
import warnings
import logging
import json

from obspy.core.inventory.util import Comment as obspy_comment

from .functions import str_indent
from .person import Persons
from .oi_date import OIDate
from .obsinfo_class_list import ObsinfoClassList

warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
logger = logging.getLogger("obsinfo")


class Comments(ObsinfoClassList):
    """
    A list of Comment objects
    """
    def __init__(self, attributes_list):
        """
            Args:
                attributes_list: (list of dict or str): list
                    of comments read from YAML/JSON file
        """
        if attributes_list is None:
            super().__init__([], Comment)
        else:
            super().__init__([Comment(x) for x in attributes_list], Comment)

    @classmethod
    def from_extras(cls, extras_dict):
        """
        Create Comments from "extras" (freeform dict object)
        """
        if extras_dict is None:
            return cls(None)
        else:
            return cls(['Extra attributes: ' + json.dumps(extras_dict)])


class Comment(object):
    def __init__(self, attributes_dict):
        if isinstance(attributes_dict, str):
            self.value = attributes_dict
            self.authors = Persons(None)
            self.begin_effective_time = OIDate(None)
            self.end_effective_time = OIDate(None)
            self.id = None
            self.subject = None
        else:
            self.value = attributes_dict.pop('value')
            self.authors = Persons(attributes_dict.pop('authors', None))
            self.begin_effective_time = OIDate(attributes_dict.pop('begin_effective_time', None))
            self.end_effective_time = OIDate(attributes_dict.pop('end_effective_time', None))
            self.id = attributes_dict.pop('id', None)
            self.subject = attributes_dict.pop('subject', None)

    def __str__(self, indent=0, n_subclasses=0):
        if n_subclasses < 0:
            return(f'{self.__class__.__name__}: {self.value}')
        s = 'Comment:\n'
        s += f'    value: {self.value}'
        if len(self.authors) > 0:
            s += f'\n    authors: {self.authors.__str__(indent=4, n_subclasses=n_subclasses-1)}'
        if self.begin_effective_time.to_obspy() is not None:
            s += f'\n    begin_effective_time: {self.begin_effective_time}'
        if self.end_effective_time.to_obspy() is not None:
            s += f'\n    end_effective_time: {self.end_effective_time}'
        if self.id is not None:
            s += f'\n    id: {self.id}'
        if self.subject is not None:
            s += f'\n    subject: {self.subject}'
        return str_indent(s, indent)

    def to_obspy(self):
        return obspy_comment(
            value=self.value,
            begin_effective_time=self.begin_effective_time.to_obspy(),
            end_effective_time=self.end_effective_time.to_obspy(),
            authors=self.authors.to_obspy(),
            subject=self.subject
        )
