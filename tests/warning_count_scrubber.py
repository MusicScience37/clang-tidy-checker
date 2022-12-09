"""Scrubber of numbers of warnings.
"""

import re


def scrub_warning_count(inputs: str) -> str:
    """Replace numbers of warnings.

    Args:
        inputs (str): Input.

    Returns:
        str: Output.
    """

    temp = re.sub(r"\d+ warnings generated\.", "<count> warnings generated.", inputs)
    return re.sub(r"\d+ warnings and ", "<count> warnings and ", temp)


WARNING_COUNT_SCRUBBER = scrub_warning_count
