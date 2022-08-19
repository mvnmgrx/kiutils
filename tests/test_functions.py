"""Helper functions for the unittests

Authors:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0
"""

import filecmp


def to_file_and_compare(object, expected_output_file: str) -> bool:
    """Write the object to a file using its `to_file()` method and comparing the output with 
    the given expected output supplied by a file with `.expected` suffix

    Args:
        object: KiUtils object with a `to_file()` method
        expected_output_file (str): Path to the file holding the expected testoutput (without `.expected` at the end)

    Returns:
        bool: True, if both the output of `to_file()` and the given expected output are the same
    """
    # Create S-Expression from object
    object.to_file(f'{expected_output_file}.testoutput')

    # Compare with the expected result
    return filecmp.cmp(f'{expected_output_file}.testoutput', f'{expected_output_file}.expected')
