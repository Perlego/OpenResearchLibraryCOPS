import os
import sys
from pprint import pprint

import jinja2
from sickle import Sickle
from sickle.models import Record

from src import utils
from src.contants import TEMPLATE_FILE, LOCAL_DIR, BOOK_TEMPLATE
from src.fields_parser import parse_creator, parse_title, parse_language, parse_isbn, parse_subject, parse_format, \
    parse_description, parse_publisher, parse_date
from src.utils import generate_product_reference, get_parameter

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

def parse_metadata_record(metadata: dict) -> dict:
    book = BOOK_TEMPLATE.copy()
    book['isbn13'] = parse_isbn(metadata['identifier'])
    book['title.title_text'] = parse_title(metadata['title'])
    book['language_of_text'] = parse_language(metadata['language'])
    book['bisacs'] = parse_subject(metadata['subject'])
    book['format'] = parse_format(metadata['format'])
    book['contributors'] = parse_creator(metadata['creator'])
    book['main_description.text'] = parse_description(metadata['description'])
    book['publisher_name'] = parse_publisher(metadata['publisher'])
    book['publication_date'] = parse_date(metadata['date'])
    book['allowed_countries'] = []
    book['record_reference'] = generate_product_reference(book['format'], book['isbn13'])
    return book


def render_template(book: dict) -> bool:
    """
    Takes book representation, call match OAI and ONIX fields and render jinja2 template, based on results.
    Args:
        book: book from OAI
    Returns:
        True if template was successfully rendered, else False
    """
    path = os.path.dirname(__file__)
    template_loader = jinja2.FileSystemLoader(searchpath=path)
    env = jinja2.Environment(loader=template_loader)
    template = env.get_template(TEMPLATE_FILE)
    env.globals[
        "get_parameter"
    ] = (
        get_parameter
    )  # map utility function from utils/ to get parameter from nested dict

    header, product = utils.render_book(book)  # call matching excel and onix fields
    output_text = template.render(header=header, product=product)
    output_file_name = f"{LOCAL_DIR}{book['isbn13']}.xml"
    with open(output_file_name, "w") as output_file:
        output_file.write(output_text)
    return True


if __name__ == '__main__':
    sickle = Sickle('https://catalog.openresearchlibrary.org/oai')
    records = sickle.ListRecords(metadataPrefix='oai_dc')

    record: Record = records.next()
    book = parse_metadata_record(record.metadata)
    render_template(book)

"""
{'creator': ['Reinisch, Jessica'],
 'date': ['2013-01-01T00:00:00Z'],
 'description': ['When the war was over in 1945, '],
 'format': ['application/pdf'],
 'identifier': ['https://openresearchlibrary.org/viewer/9fa24158-ec43-4b6f-9c99-f8edd0e5b260',
                'https://openresearchlibrary.org/ext/api/media/9fa24158-ec43-4b6f-9c99-f8edd0e5b260/assets/external_content.pdf',
                'ISBN:9780199660797',
                'DOI:https://dx.doi.org/10.1093/acprof:oso/9780199660797.001.0001'],
 'language': ['English'],
 'publisher': ['Oxford University Press'],
 'rights': ['https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'],
 'source': ['MODID-7e8a1317c8d:Oxford University Press - OA'],
 'subject': ['History / Military / World War Ii',
             'bisacsh:HIS027100',
             'History / Europe',
             'bisacsh:HIS010000',
             'History / Modern / 20th Century',
             'bisacsh:HIS037070'],
 'title': ['The Perils of Peace'],
 'type': ['BOOK']}

Process finished with exit code 0

"""
