"""
Filter class and subclasses
"""
# Standard library modules
import logging

from .coefficients import Coefficients
from ...helpers import str_indent

logger = logging.getLogger("obsinfo")


class ADConversion(Coefficients):
    """
    ADConversion Filter (Flat Coefficients filter)

    Attributes:
        input_full_scale (float): A/D's input full scale (volts)
        output_full_scale (float): corresponding output full scale (counts)
        delay_samples (float): number of samples that the filter delays an
            impulse
    """

    def __init__(self, attributes_dict, stage_id=-1):
        """
        Constructor

        Args:
            attributes_dict (dict or :class:`.ObsMetadata`): filter attributes
            stage_id (int): id of corresponding stage. Used for reporting only
        """
        logger.debug(f'in {self.__class__.__name__}.__init__()')
        attributes_dict["transfer_function_type"] = 'DIGITAL'
        attributes_dict["numerator_coefficients"] = [1.0]
        attributes_dict["denominator_coefficients"] = []
        # Have to pop these before super, or it will give an error.
        input_full_scale = attributes_dict.pop('input_full_scale', None)
        output_full_scale = attributes_dict.pop('output_full_scale', None)
        super().__init__(attributes_dict, stage_id)
        self.input_full_scale = input_full_scale
        self.output_full_scale = output_full_scale
        self._validate_empty_attributes_dict(attributes_dict)

    def __str__(self, indent=0, n_subclasses=0):
        if n_subclasses < 0:
            return f'{type(self)}'
        s = super().__str__() + '\n'
        s += '    input_full_scale: {self.input_full_scale}\n'
        s += '    output_full_scale: {self.output_full_scale}'
        return str_indent(s, indent)

