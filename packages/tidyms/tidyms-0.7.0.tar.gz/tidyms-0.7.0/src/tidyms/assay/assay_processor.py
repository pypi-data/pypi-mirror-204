"""
Tools to process Assay data.

"""
from abc import ABC, abstractmethod
from .assay_data import AssayData, Sample
from .. import _constants as c
from .. import validation as val

from typing import Any

PROCESSING_ORDER = [c.DETECT_FEATURES, c.EXTRACT_FEATURES, c.MATCH_FEATURES, c.MAKE_DATA_MATRIX]

class PreprocessingOrderError(ValueError):
    """
    Exception raised when the preprocessing methods are called in the wrong order.

    """

    pass


class AssayProcessor(ABC):

    parameters: dict
    step: str
    schema: dict

    def __init__(self, step: str, separation: str, instrument: str, **kwargs):

        if separation not in c.SEPARATION_MODES:
            valid_separation = ", ".join(c.SEPARATION_MODES)
            msg = f"{separation} is not a valid separation mode. Valid values are: {valid_separation}."
            raise ValueError(msg)
        
        if instrument not in c.MS_INSTRUMENTS:
            valid_instruments = ", ".join(c.MS_INSTRUMENTS)
            msg = f"{instrument} is not a valid MS instrument. Valid values are: {valid_instruments}."
            raise ValueError(msg)

        if step not in c.PREPROCESSING_STEPS:
            valid_steps = ", ".join(c.PREPROCESSING_STEPS)
            msg = f"{step} is not a valid preprocessing step. Valid values are: {valid_steps}."
            raise ValueError(msg)
        
        self.separation = separation
        self.instrument = instrument
        self.step = step
        self._validate_parameters(kwargs)
        self.parameters = kwargs

    def _validate_parameters(self, parameters: dict):
        schema = self._get_parameter_schema()
        defaults = self._get_default_parameters()
        # TODO : replace defaults
        validator = val.ValidatorWithLowerThan(self.schema)
        val.validate(parameters, validator)

    @abstractmethod
    def _get_default_parameters(self) -> dict[str, Any]:
        ...

    @abstractmethod
    def _get_parameter_schema(self) -> dict[str, Any]:
        ...
        
    def _store_parameters(self, data: AssayData):
        data.set_processing_parameters(self.step, self.parameters)

    @abstractmethod
    def process(self):
        ...

    @abstractmethod
    def func(self):
        ...

    def check_step(self, data: AssayData):
        all_samples = data.get_samples()
        step_index = PROCESSING_ORDER.index(self.step)
        if step_index > 0:
            previous_step = PROCESSING_ORDER[step_index - 1]
            processed_samples = data.get_samples(step=previous_step)
            check_okay = set(all_samples) == set(processed_samples)
        else:
            check_okay = True

        if not check_okay:
            msg = f"{previous_step} method must be applied on Assay before applying {self.step}."
            raise PreprocessingOrderError(msg)



class RoiExtractor(AssayProcessor):

    def _get_parameter_schema(self) -> dict[str, Any]:
        schema = {
            "tolerance": {"type": "number", "is_positive": True},
            "max_missing": {"type": "integer", "min": 0},
            "targeted_mz": {"nullable": True, "check_with": is_all_positive},
            "multiple_match": {"allowed": ["closest", "reduce"]},
            "mz_reduce": {
                "anyof": [
                    {"allowed": ["mean"]},
                    {"check_with": is_callable}
                ]
            },
            "sp_reduce": {
                "anyof": [
                    {"allowed": ["mean", "sum"]},
                    {"check_with": is_callable}
                ]
            },
            "min_intensity": {
                "type": "number",
                "min": 0.0,
                "nullable": True
            },
            "min_length": {
                "type": "integer",
                "min": 1,
                "nullable": True,
            },
            "pad": {
                "type": "integer",
                "min": 0,
                "nullable": True,
            },
            "ms_level": {
                "type": "integer",
                "min": 1,
            },
            "start_time": {
                "type": "number",
                "min": 0.0,
                "lower_than": "end_time",
            },
            "end_time": {
                "type": "number",
                "nullable": True,
            },
            "min_snr": {
                "type": "number",
                "is_positive": True,
            },
            "min_distance": {
                "type": "number",
                "is_positive": True,
            }
        }

    def process(self, data: AssayData):
        sample_list = data.