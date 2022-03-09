"""Functions for string manipulation

Author:
    (C) Marvin Mager - @mrnmgrx - 2022

Major changes:
    28.02.2022 - created
"""

def dequote(input: str) -> str:
    """Escapes double-quotes in a string using a backslash

    Args:
        input (str): String to replace double-quotes

    Returns:
        str: String with replaced double-quotes
    """
    return input.replace("\"", "\\\"")