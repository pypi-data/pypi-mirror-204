"""
Python equivalent of obspy FloatWithUncertaintiesFixedUnit class
"""
# Standard library modules
import warnings
import logging

# Non-standard modules
from obspy.core.util.obspy_types import (FloatWithUncertaintiesFixedUnit,
                                         FloatWithUncertaintiesAndUnit)


warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
logger = logging.getLogger("obsinfo")


class FloatWithUncert(object):
    """
    Python equivalent of obspy FloatWithUncertaintiesFixedUnit and
    FloatWithUncertaintiesAndUnit

    Attributes:
        value (float): float value
        uncertainty (float): uncertainty in value
        measurement_method (str): measurement method
    """

    def __init__(self, attributes_dict):
        """
        Create object and assign attributes from attributes_dict.

        Args:
            attributes_dict (dict or :class:`ObsMetadata`): dict with
                relevangt keys
        """
        self.value = attributes_dict['value']        # required
        self.uncertainty = attributes_dict.get('uncertainty', None)
        self.measurement_method = attributes_dict.get('measurement_method',
                                                      None)
        self.unit = attributes_dict.get('unit', None)

    def __str__(self, indent=0, n_subclasses=0):
        """ Writes everything out, one line, no subclasses """
        s = 'FloatWithUncert: {} +- {}'.format(self.value, self.uncertainty)
        if self.unit is not None:
            s += f' {self.unit}'
        if self.measurement_method is not None:
            s += f', measurement_method = {self.measurement_method}'
        return s

    def __repr__(self, no_title=False):
        """
        Args:
            no_title (bool): don't surround dict with 'FloatWithUncert()'
        """
        args = [f"'value': {self.value}"]
        if self.uncertainty:
            args.append(f"'uncertainty': {self.uncertainty}")
        if self.measurement_method:
            args.append(f"'measurement_method': '{self.measurement_method}'")
        if self.unit:
            args.append(f"'unit': '{self.unit}'")
        dict_string = '{' + ", ".join(args) + '}'
        if no_title:
            return dict_string
        return 'FloatWithUncert(' + dict_string + ')'

    def to_obspy(self):
        """
        Return obspy object:
          - FloatWithUncertaintiesFixedUnit if unit=None
          - FloatWithUncertaintiesAndUnit otherwise
        """
        if self.unit is None:
            return FloatWithUncertaintiesFixedUnit(
                value=self.value,
                lower_uncertainty=self.uncertainty,
                upper_uncertainty=self.uncertainty,
                measurement_method=self.measurement_method)
        else:
            return FloatWithUncertaintiesAndUnit(
                value=self.value,
                lower_uncertainty=self.uncertainty,
                upper_uncertainty=self.uncertainty,
                measurement_method=self.measurement_method,
                unit=self.unit)
