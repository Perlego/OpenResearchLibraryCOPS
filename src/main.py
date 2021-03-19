import ast
import os
import sys

import boto3
import jinja2
import requests
from sickle import Sickle

from src import utils
from src.contants import TEMPLATE_FILE, LOCAL_DIR, BOOK_TEMPLATE
from src.fields_parser import (
    parse_creator,
    parse_title,
    parse_language,
    parse_isbn,
    parse_subject,
    parse_format,
    parse_description,
    parse_publisher,
    parse_date,
    parse_download_link,
    parse_book_identifier,
)
from src.utils import generate_product_reference, get_parameter, upload_object_by_path, delete_local_file

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)


def parse_metadata_record(metadata: dict) -> dict:
    book = BOOK_TEMPLATE.copy()
    book["isbn13"] = parse_isbn(metadata["identifier"])
    book["title.title_text"] = parse_title(metadata["title"])
    book["language_of_text"] = parse_language(metadata["language"])
    book["bisacs"] = parse_subject(metadata["subject"]) if "subject" in metadata else [""]
    book["format"] = parse_format(metadata["format"])

    if "creator" in metadata:
        author = parse_creator(metadata["creator"])
    elif "contributor" in metadata:
        author = parse_creator(metadata["contributor"])
    else:
        author = ""
    book["contributors"] = author

    book["main_description.text"] = parse_description(metadata["description"]) if "description" in metadata else ""
    book["publisher_name"] = parse_publisher(metadata["publisher"])
    book["publication_date"] = parse_date(metadata["date"])
    book["allowed_countries"] = "WORLD"
    book["record_reference"] = generate_product_reference(book["format"], book["isbn13"])
    return book


def render_template(book: dict) -> str:
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
    env.globals["get_parameter"] = get_parameter  # map utility function from utils/ to get parameter from nested dict

    header, product = utils.render_book(book)  # call matching excel and onix fields
    output_text = template.render(header=header, product=product)
    output_file_name = f"{LOCAL_DIR}/{book['isbn13']}.xml"
    with open(output_file_name, "w") as output_file:
        output_file.write(output_text)
    print(f"Metadata file {book['isbn13']}.xml was successfully downloaded to {output_file_name}")
    return output_file_name


def download_metadata(metadata: dict) -> str:
    book = parse_metadata_record(metadata)
    if len(book["isbn13"]) < 2:
        return ""
    metadata_file_path = render_template(book)
    return metadata_file_path


def download_book_prepare_data(metadata: dict):
    url = parse_download_link(metadata["identifier"])
    isbn = parse_isbn(metadata["identifier"])
    book_format = parse_format(metadata["format"])
    return {"url": url, "isbn": isbn, "book_format": book_format}


def download_book(prepared_data: dict) -> str:
    req = requests.get(prepared_data["url"])
    file_name = f"{prepared_data['isbn']}.{prepared_data['book_format'].lower()}"
    file_path = f"./books/{file_name}"
    with open(file_path, "wb") as f:
        f.write(req.content)

    # Retrieve HTTP meta-data
    if req.status_code == 200:
        print(f"Book file {file_name} was successfully downloaded to {file_path}")
    return file_path


def prepare_download_cover_data(metadata: dict) -> dict:
    book_identifier = parse_book_identifier(metadata["identifier"])
    return {
        "url": f"https://openresearchlibrary.org/ext/api/media/{book_identifier}/assets/thumbnail.jpg",
        "isbn": parse_isbn(metadata["identifier"]),
    }


def download_cover(prepared_data: dict) -> str:
    req = requests.get(prepared_data["url"])
    file_name = f"{prepared_data['isbn']}.jpg"
    file_path = f"./images/{file_name}"
    with open(file_path, "wb") as f:
        f.write(req.content)

    # Retrieve HTTP meta-data
    if req.status_code == 200:
        print(f"Cover file {file_name} was successfully downloaded to {file_path}")
    return file_path


def get_metadata(record: dict, s3) -> None:
    """
    Prepare metadata, download metadata, upload it to S3 and delete local file
    """
    metadata_file_path = download_metadata(record)
    metadata_file_name = metadata_file_path.split("/")[-1]
    upload_object_by_path(
        s3,
        s3_path=f"content/open_research_library_iudilif/{metadata_file_name}",
        local_path=metadata_file_path,
        bucket_name="plgo-ebooks-bucket",
    )
    delete_local_file(metadata_file_path)


def get_book(record: dict, s3) -> None:
    """
    Prepare book data, download book, upload it to S3 and delete local file
    """
    book_download_data = download_book_prepare_data(metadata=record)
    book_file_path = download_book(book_download_data)
    book_file_name = book_file_path.split("/")[-1]
    upload_object_by_path(
        s3,
        s3_path=f"content/open_research_library_iudilif/{book_file_name}",
        local_path=book_file_path,
        bucket_name="plgo-ebooks-bucket",
    )
    delete_local_file(book_file_path)


def get_cover(record: dict, s3) -> None:
    """
    Prepare cover data, download cover, upload it to S3 and delete local file
    """
    cover_download_data = prepare_download_cover_data(metadata=record)
    cover_file_path = download_cover(cover_download_data)
    cover_file_name = cover_file_path.split("/")[-1]
    upload_object_by_path(
        s3,
        s3_path=f"content/open_research_library_iudilif/{cover_file_name}",
        local_path=cover_file_path,
        bucket_name="plgo-ebooks-bucket",
    )
    delete_local_file(cover_file_path)


def process_books_from_file():
    """
    Read all records from file and parse them one by one, getting metadata, book and cover for every record
    """
    with open("/home/aviaowl/PycharmProjects/OpenResearchLibraryCOPS/src/output_right.csv") as output:
        lines = output.readlines()

    prod = boto3.session.Session(profile_name="prod")
    s3 = prod.resource("s3")

    for line in lines:
        record = ast.literal_eval(line.strip())
        if record["type"][0] == "BOOK":
            get_metadata(record, s3)
            get_book(record, s3)
            get_cover(record, s3)


def parse_oai_archive_to_file() -> None:
    """
    Get all records from OAI Archive and save them to csv file
    """
    sickle = Sickle("https://catalog.openresearchlibrary.org/oai")
    records = sickle.ListRecords(metadataPrefix="oai_dc")
    i = 1
    with open("output_right.csv", "a") as f1:
        for record in records:
            if record.metadata["type"][0] == "BOOK":
                i += 1
                print(f"{i} book")
                f1.write(f"{record.metadata}\n")


if __name__ == "__main__":
    parse_oai_archive_to_file()
    process_books_from_file()
