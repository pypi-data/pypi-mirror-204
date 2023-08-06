"""
Station Class
"""
# Standard library modules
import warnings
import logging

from obspy.core.inventory.util import Site as obspy_site

from ..helpers import str_indent

warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
logger = logging.getLogger("obsinfo")


class Site(object):
    def __init__(self, name):
        self.name = name
        
    def __str__(self, indent=0, n_subclasses=0):
        return str_indent(f'Site: {self.name}', indent)
    
    def to_obspy(self):
        return obspy_site(name=self.name, description=None, town=None, county=None,
                    region=None, country=None)