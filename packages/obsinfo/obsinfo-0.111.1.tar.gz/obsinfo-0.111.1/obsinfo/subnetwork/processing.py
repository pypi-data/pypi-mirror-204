"""
Processing Class, holds list of data processing steps
"""

# Standard library modules
import warnings
import logging
import json

# Non-standard modules

# obsinfo modules
from ..helpers import str_indent, str_list_str, Comments

warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
logger = logging.getLogger("obsinfo")


class Processing(object):
    """
    No equivalent class in obspy/StationXML

    Saves a list of Processing steps as strings
    For now, just stores the list. Will be converted to StationXML comments

    Attributes:
        processing_list (list): list of processing steps with attributes,
            either linear_drift or leapsecond

    """

    def __init__(self, attributes):
        """
        Constructor

        Args:
        attributes (list): list of processing steps (linear_drift or
            leapsecond) with attributes
        """

        self.processing_list = []

        if not attributes:
            return

        # make it a list for standard processing if user forgot the dash
        if not isinstance(attributes, list):
            attributes = [attributes]

        # Wayne added self.attributes to allow makescript_LC2SDS
        self.attributes = attributes

        for attr in attributes:
            try:
                js = json.dumps(attr)
                self.processing_list.append(js)
            except TypeError as e:
                msg = f'json.dumps() error: {e}, could not put processing action {attr} in comments'

    def __repr__(self):
        s = f'Processing({self.processing_list})'
        return s

    def __str__(self, indent=0, n_subclasses=0):
        if n_subclasses < 0:
            return f'{self.__class__.__name__}'
        kwargs = dict(indent=4, n_subclasses=n_subclasses-1)
        s = f'{self.__class__.__name__}:\n'
        s += f'    {str_list_str(self.processing_list, **kwargs)}'
        return str_indent(s, indent)
        
    def to_comments(self):
        """Returns processing list as Comments"""
        return Comments(self.processing_list)