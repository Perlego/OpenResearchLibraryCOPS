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
    print(f"Name: {raw_creator}")
    if not isinstance(raw_creator, List):
        print(f"WARNING: Wrong input type: '{type(raw_creator)}', expected List")
        return ""
    for creator in raw_creator:
        # Format names like 'Potter, Harry' to 'Harry Potter'
        if not isinstance(creator, str):
            print(f"WARNING: non-string creator value: {creator}. Skipping...")
            continue
        if "," in creator and len(creator.split(",")) == 2:
            surname, name = creator.split(",")
            formatted_names.append(f"{name.strip()} {surname.strip()}")
        else:
            if len(creator) > 0:
                formatted_names.append(creator)
    return ", ".join(formatted_names)


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
        print(
            f"Error during parsing publishing date: {raw_date}(Wrong date format?). Returning default date: 20210101"
        )
        final_date = default_date
    return final_date


def parse_description(raw_description: List[str]) -> str:
    """
    Parses description and return description text
    Returns:
        String, contains first value of the input list
        or empty string in case of errors
    """
    if (
            not isinstance(raw_description, List)
            or not raw_description
            or not isinstance(raw_description[0], str)
            or len(raw_description[0]) == 0
    ):
        print(f"WARNING: found wrong description: {raw_description}")
        return ""
    return raw_description[0]


def parse_format(raw_format: List[str]) -> str:
    """
    Parse and validate format
    Args:
        raw_format: List contains one string with format
    Returns:
        upper-case format or empty string if format isn't supported
    Examples:
        Input: ['application/pdf']
        Output: PDF
    """
    if not raw_format or not isinstance(raw_format, List):
        print(f"WARNING: Wrong format: {raw_format}. Skipping...")
        return ""
    final_format = ""
    if "pdf" in raw_format[0].lower():
        final_format = "PDF"
    elif "epub" in raw_format[0].lower():
        final_format = "EPUB"
    else:
        print(f"WARNING: Unknown format: {raw_format[0]}. Skipping...")
    return final_format


def parse_isbn(raw_identifier: List[str]) -> str:
    """
    Parse and validate ISBN from raw identifier list
    Args:
        raw_identifier: list of identifiers, contains download link and/or viewer link, ISBN and DOI
    Returns:
        parsed and verified ISBN or empty string
    Examples:
        Input: ['https://openresearchlibrary.org/viewer/9fa24158-ec43-4b6f-9c99-f8edd0e5b260',
                'https://openresearchlibrary.org/ext/api/media/9fa24158-ec43-4b6f-9c99-f8edd0e5b260/assets/external_content.pdf',
                'ISBN:9780199660797',
                'DOI:https://dx.doi.org/10.1093/acprof:oso/9780199660797.001.0001']
        Output:
            9780199660797
    """
    raw_isbn = [element.split(":")[-1] for element in raw_identifier if "isbn" in element.lower()]
    if len(raw_isbn) == 0:
        print(f"WARNING: ISBN not found in input: {raw_identifier}")
        return ""
    elif len(raw_isbn) > 1:
        print(f"WARNING: More than one ISBN were found: {raw_isbn}")
        return ""
    else:
        isbn = raw_isbn[0]
    if isbn.isnumeric() and len(isbn) == 13 and isbn.startswith("97"):
        return isbn
    else:
        # print(f"WARNING: wrong ISBN: {isbn}, check that length and format")
        return ""


def parse_book_identifier(raw_identifier: List[str]) -> str:
    viewer_link = [element for element in raw_identifier if "viewer" in element.lower()][0]
    book_identifier = viewer_link.split('/')[-1]
    return book_identifier


def parse_download_link(raw_identifier: List[str]) -> str:
    """
    Parse list of identificators and find download link. If download link not found, generate one from book viewer link
    Args:
        raw_identifier: list of identifiers, contains download link and/or viewer link, ISBN and DOI
    Returns:
        Link to download book
    """
    if not raw_identifier or not isinstance(raw_identifier, List):
        print(f"WARNING: wrong identifier: {raw_identifier}")
        return ""
    links = [element for element in raw_identifier if "external_content" in element.lower()]
    if not links:
        book_identifier = parse_book_identifier(raw_identifier)
        download_link = f"https://openresearchlibrary.org/ext/api/media/{book_identifier}/assets/external_content.pdf"
    else:
        download_link = links[0]
    return download_link


def parse_language(raw_language: List[str]) -> str:
    """
    Parse language and return language code to insert it to metadata
    Returns:
        language_id from main database according to language reference or empty code
    Examples:
        Input: ['English']
        Output: "1"
    """
    if not raw_language or not isinstance(raw_language, List):
        print(f"WARNING: wrong language: {raw_language}")
        return ""
    return raw_language[0]


def parse_publisher(raw_publisher: List[str]) -> str:
    """
    Parse publisher data
    Args:
        raw_publisher: List of publishers
    Returns:
        Parsed publihser (first element of input list) or empty string
    Examples:
        Input: ['Oxford University Press']
        Output: 'Oxford University Press'
    """
    if not raw_publisher or not isinstance(raw_publisher, List):
        print(f"WARNING: wrong publisher: {raw_publisher}")
        return ""
    return str(raw_publisher[0])


def parse_title(raw_title: List[str]) -> str:
    """
    Args:
        raw_title: list contains title
    Returns:
        parsed title or empty string
    """
    if not raw_title or not isinstance(raw_title, List):
        print(f"WARNING: wrong title: {raw_title}")
        return ""
    return str(raw_title[0])


def parse_subject(raw_subject: List[str]) -> List[str]:
    """
    Args:
        raw_subject: List of subject, rows contains BISAC codes and subject_name
    Returns:
        List of BISAC codes
    Examples:
        Input: ['History / Military / World War Ii',
             'bisacsh:HIS027100',
             'History / Europe',
             'bisacsh:HIS010000',
             'History / Modern / 20th Century',
             'bisacsh:HIS037070']
        Output:
            ['HIS027100', 'HIS010000', 'HIS037070']
    """
    if not raw_subject or not isinstance(raw_subject, List):
        print(f"WARNING: wrong subject: {raw_subject}")
        return []
    bisacs = []
    for subject in raw_subject:
        if subject.startswith("bisacsh"):
            bisacs.append(subject.split('bisacsh:')[-1])
    return bisacs
