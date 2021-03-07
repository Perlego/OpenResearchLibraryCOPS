from typing import List

import dateutil.parser as date_parser

from src.contants import ONIX_DATE_FORMAT


def parse_creator(raw_creator: List[str]) -> str:
    """
    Parses list of creators.
    Args:
        raw_creator: List of strings. Based on source data, asssuming that each name has the format: 'surname, name'
    Returns:
        Row, contains all authors, separated by comma. Each author name formatted as 'name surname'
    Examples:
        Input: ['Potter, Harry', 'Granger, Hermione']
        Output: 'Harry Potter, Hermione Granger'
    """
    formatted_names = []
    if not isinstance(raw_creator, List):
        print(f"WARNING: Wrong input type: '{type(raw_creator)}', expected List")
        return ""
    for creator in raw_creator:
        # Format names like 'Potter, Harry' to 'Harry Potter'
        if not isinstance(creator, str):
            print(f"WARNING: non-string creator value: {creator}. Skipping...")
            continue
        if ',' in creator:
            surname, name = creator.split(',')
            formatted_names.append(f'{name.strip()} {surname.strip()}')
        else:
            if len(creator) > 0:
                formatted_names.append(creator)
    return ', '.join(formatted_names)


def parse_date(raw_date: List[str]) -> str:
    """
    Args:
        raw_date:
            List contains single date in format YYYY-MM-DDT:HH:MM:SSZ
    Returns:
        String representation of date in format YYYYMMDD.
        In case of errors returns default date 20210101
    Examples:
        Input: ['2013-01-01T00:00:00Z']
        Output: '20130101'
    """
    default_date = "20210101"
    if not isinstance(raw_date, List) or not raw_date[0]:
        print(f"WARNING: Wrong publishing date: {raw_date}, expected: List[str]")
        return default_date
    try:
        final_date = date_parser.parse(raw_date[0]).strftime(ONIX_DATE_FORMAT)
    except OverflowError:
        print(f"Error during parsing publishing date: {raw_date}(Wrong date format?). Returning default date: 20210101")
        final_date = default_date
    return final_date


def parse_description(raw_description: List[str]) -> str:
    """
    Parses description and return description text
    Returns:
        String, contains first value of the input list
        or empty string in case of errors
    """
    if not isinstance(raw_description, List) or not isinstance(raw_description[0], str) or len(raw_description[0]) == 0:
        print(f"WARNING: found wrong description: {raw_description}")
        return ""
    return raw_description[0]


def parse_format():
    """
    TODO
    Returns:

    """
    pass


def parse_identifier():
    """
    TODO
    Returns:

    """
    pass


def parse_language():
    """
    TODO
    Returns:

    """
    pass


def parse_publisher():
    """
    TODO
    Returns:

    """
    pass


def parse_subject():
    """
    TODO
    Returns:

    """
    pass


def parse_title():
    """
    TODO
    Returns:

    """
    pass
