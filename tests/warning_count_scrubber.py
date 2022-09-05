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

    return re.sub(r"(\d+) warnings generated\.", "<count> warnings generated.", inputs)


WARNING_COUNT_SCRUBBER = scrub_warning_count
