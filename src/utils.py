from datetime import datetime
from typing import Tuple

from src.contants import ONIX_DATE_FORMAT


def get_contributors_dict(contributors: str) -> dict:
    """
    Args:
        contributors: string with authors, separated by comma
    Returns:
        dict with all necessary contributors fields for ONIX
    Examples:
        Input: ['Harry Potter, Hermione Granger']
        Output: [{'contributor_role': 'A01', 'person_name': 'Harry Potter, Hermione Granger', 'sequence_number': '1'}]
    """
    return [dict(contributor_role="A01", person_name=contributors, sequence_number='1')]


def generate_product_reference(book_format: str, isbn: str) -> str:
    """
    Args:
        book_format: valid book format: PDF or EPUB
        isbn: parsed and validated book ISBN
    Returns:
        record reference
    Examples:
        Input: EPUB, 9780199660797
        Output: 9780199660797.epub
    """
    if len(isbn) > 0 and book_format.strip().lower() in ("pdf", "epub"):
        return f"{isbn}.{book_format.strip().lower()}"
    else:
        print(f"WARNING: wrong input: {book_format, isbn}. Check that isbn is not empty and book format is supported")
        return ""


def get_key_from_dict_recursively(parameter: dict, key: str):
    if key in parameter:
        return parameter[key]
    for value in parameter.values():
        if isinstance(value, dict):
            result = get_key_from_dict_recursively(value, key)
            if result and result != "":
                return result


def get_parameter(parameter: dict, key: str, default: str) -> str:
    """Recursively search for a key in nested dictionary
    Args:
        parameter: nested dictionary, where we need to find a key
        key: key to search
        default: default value if key not found
    Returns:
        value of the determined key from the nested dict or default value
    """
    value = get_key_from_dict_recursively(parameter, key)
    if value is not None:
        return value
    return default


def render_book(book: dict) -> Tuple[dict, dict]:  # pylint: disable=too-many-locals
    """
    Takes validated book and match book fields with fields of jinja2 template, repeat xml structure
    Args:
        book: book to render
    Examples:
        output >>
        {'sent_date_time': '20200809'}   # header
        {'record_reference': '9788429194098.epub',  # product
        'descriptive_detail': {'title_detail': {'title_element': ...
    Returns:
        rendered header and product of the book
    """
    # header part
    today = datetime.today().date().strftime(ONIX_DATE_FORMAT)
    header = dict(sent_date_time=today)

    # product part
    product_identifier = dict(product_id_value=book["isbn13"])

    # descriptive detail
    title_element = dict(title_text=book["title.title_text"])
    title_detail = dict(title_element=title_element)
    language = dict(language_code=book["language_of_text"])
    subject = dict(subject_code=book["bisacs"][0])
    product_form_code = "E107" if book["format"] == "PDF" else "E101"

    descriptive_detail = dict(
        title_detail=title_detail,
        contributors=get_contributors_dict(book['contributors']),
        language=language,
        subject=subject,
        product_form_detail=product_form_code,
    )

    # collateral detail
    collateral_detail = dict(text_content_text=book["main_description.text"])

    # publishing detail
    publisher = dict(publisher_name=book["publisher_name"])
    publishing_date = dict(publishing_date_date=book["publication_date"])
    sales_rights = dict(countries_included=book["allowed_countries"])

    publishing_detail = dict(
        publisher=publisher,
        publishing_date=publishing_date,
        sales_rights=sales_rights,
    )

    # product supply
    supplier = dict(supplier_name="Open Research Library")
    price = dict(
        currency_code="GBP",
        price_amount="0",
        price_type="01",
    )
    product_supply = dict(
        supplier=supplier,
        product_availability="20",
        price=price,
    )

    # final product
    product = dict(
        record_reference=book["record_reference"],
        notification_type="03",
        product_identifier=product_identifier,
        descriptive_detail=descriptive_detail,
        collateral_detail=collateral_detail,
        publishing_detail=publishing_detail,
        product_supply=product_supply,
    )
    return header, product
