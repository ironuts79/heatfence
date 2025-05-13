from typing import Iterable
from result import Result, Err, Ok
from sensors import FeatureIterator, get_label, get_value

#
def read_sensor_by_label(chip: object, labels: Iterable or str) -> Result:
    retval = {}

    # move simple string to iterable
    if isinstance(labels, str): 
        labels = [labels]

    try:
        for feature in FeatureIterator(chip):
            for label in labels:
                if not label:
                    raise ValueError('label cant be an empty string')

                if get_label(chip, feature) == label:
                    retval[label.replace(' ', '_').lower()] = get_value(chip, feature.number)
        return Ok(retval)

    except Exception as e:
        return Err(e)