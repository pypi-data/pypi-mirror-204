"""
Orientation class
"""
# Standard library modules
import warnings
import logging

# Non-standard modules
import obspy.core.util.obspy_types as obspy_types

# obsinfo modules
from ..obsmetadata import (ObsMetadata)
from ..helpers import FloatWithUncert, str_indent

warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
logger = logging.getLogger("obsinfo")


class Orientation(object):
    """
    Class for sensor orientations. No channel modifs. Cannot change orientation
    as it is part of the channel identifiers. Azimuth and dip can be changed
    Orientation is coded by `FDSN standard <http://docs.fdsn.org/projects/
    source-identifiers/en/v1.0/channel-codes.html>`
    
    These are the dips to give for vertical/hydrophone channels:
        -90°:
            - vertical seismometer with positive voltage corresponding to
              upward motion (typical seismometer)
            - hydrophone with positive voltage corresponding to increase
              in pressure (compression)
         90°: vertical seismometer with positive voltage corresponding to
              downward motion (typical geophone),
            - hydrophone with positive voltage corresponding to decrease
              in pressure (dilatation)

    Attributes:
        code (str): Single-letter orientation code
        azimuth (:class:`FloatWithUncert`): azimuth in degrees, clockwise from
            north
        dip (:class:`FloatWithUncert`): dip in degrees, -90 to 90, positive=down,
            negative=up
    """

    def __init__(self, attributes_dict):
        """
        Constructor

        Args:
            attributes_dict (dict or :class:`.ObsMetadata`): Orientation
                dictionary with key = orientation code
        """

        if not attributes_dict:
            msg = 'No orientation'
            warnings.warn(msg)
            logger.error(msg)
            raise ValueError(msg)

        # if a dictionary attributes_dict contains azimuth and/or dip info
        # else it's a simple string and is included in a list for generality
        # PREVIOUSLY ALLOWED ORIENTATIONS W/O AZIMUTH/DIP
        # keys = list(attributes_dict.keys()
        #             if isinstance(attributes_dict, dict) else attributes_dict)
        keys = list(attributes_dict)
        if len(keys) == 0:
            raise ValueError('No orientation code')
        elif len(keys) > 1:
            raise ValueError(f'More than one orientation code: {keys}')
        key = keys[0]
        if len(key) != 1:
            raise ValueError(f'orientation code not one character: "{key}"')
        if not key in '123HXYZEN':
            raise ValueError(f'orientation code "{key}" not in accepted list: "123HXYZEN"')
        self.code = key
        value = ObsMetadata(attributes_dict.pop(key, None))
        azimuth = value.get('azimuth.deg', None)
        dip = value.get('dip.deg', None)
        if azimuth is None and dip is None:
            raise ValueError(f'orientation {key}: neither azimuth nor dip specified')
        if azimuth is not None:
            azimuth.safe_update({'unit': 'degrees'})
            self.azimuth = FloatWithUncert(azimuth)
        else:
            self.azimuth = FloatWithUncert({'value': 0, 'unit': 'degrees'})
        if dip is not None:
            dip.safe_update({'unit': 'degrees'})
            self.dip = FloatWithUncert(dip)
        else:
            self.dip = FloatWithUncert({'value': 0, 'unit': 'degrees'})
            
        # Test required values
        if key in 'XYEN':
            if self.azimuth.uncertainty is None:
                logger.warning("orientation XYEN should have azimuth uncertainty, doesn't")
            else:
                if self.azimuth.uncertainty > 5:
                    logger.warning("{key} orientation azimuth uncertainty > 5 degrees")
            if key == 'E':
                if self.azimuth.value <85 or self.azimuth.value > 95:
                    raise ValueError('E orientation azimuth = {self.azimuth.value), not between 85 and 95')
            elif key == 'N':
                if self.azimuth.value < 355 and self.azimuth.value > 5:
                    raise ValueError('N orientation azimuth is not between 355 and 5')
        elif key == 'ZH':
            if self.azimuth.uncertainty is None:
                logger.warning("ZH orientation should have dip uncertainty, doesn't")
            else:
                if self.azimuth.uncertainty > 5:
                    logger.warning("{key} orientation dip uncertainty > 5 degrees")
            if key == 'Z':
                if self.dip.value <-90 or self.dip.value > -85:
                    raise ValueError('E orientation azimuth is not between -85 and -90')
            
    def __repr__(self):
        args=[]
        if self.azimuth.value != 0 or self.azimuth.uncertainty is not None or self.azimuth.measurement_method is not None:
            args.append(f"'azimuth': {self.azimuth.__repr__(True)}")
        if self.dip.value != 0 or self.dip.uncertainty is not None or self.dip.measurement_method is not None:
            args.append(f"'dip': {self.dip.__repr__(True)}")
        return "Orientation({" + f"'{self.code}':" + " {" + ", ".join(args) + "}})"

    def __str__(self, indent=0, n_subclasses=0):
        s = 'Orientation:\n'
        s += f'    code: {self.code}\n'
        s += f'    azimuth: {self.azimuth}\n'
        s += f'    dip: {self.dip}'
        return str_indent(s, indent)