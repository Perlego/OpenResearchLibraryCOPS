import pytest

from src.fields_parser import parse_creator, parse_date, parse_description, parse_format, parse_isbn, \
    parse_download_link, parse_language, parse_publisher, parse_subject, parse_title


@pytest.mark.parametrize("raw_creator, expected_creator", [(['Potter, Harry'], "Harry Potter"),
                                                           (['Granger, Hermione', 'Potter, Harry'],
                                                            "Hermione Granger, Harry Potter"),
                                                           (['Granger, Hermione', 'Potter, Harry', ''],
                                                            "Hermione Granger, Harry Potter"),
                                                           (['Hermione Granger', 'Harry Potter'],
                                                            "Hermione Granger, Harry Potter"),
                                                           ([None, 1234, 'Harry Potter'], "Harry Potter"),
                                                           ("Ron Weasley", "",),
                                                           (['Reagle, Jr., Joseph M.'], "Reagle, Jr., Joseph M.")])
def test_parse_creator(raw_creator, expected_creator):
    assert parse_creator(raw_creator) == expected_creator


@pytest.mark.parametrize("raw_date, expected_date", [(['2013-01-01T00:00:00Z'], '20130101'),
                                                     (['20130101'], '20130101'),
                                                     (['01.01.2013'], '20130101'),
                                                     (['06-11-1993'], '19930611'),
                                                     (['872194837902963825043'], '20210101'),
                                                     ([""], '20210101'),
                                                     (None, '20210101'),
                                                     ('2013-01-01T00:00:00Z', '20210101')])
def test_parse_date(raw_date, expected_date):
    assert parse_date(raw_date) == expected_date


@pytest.mark.parametrize("raw_description, expected_description", [(['Winter is coming'], 'Winter is coming'),
                                                                   (None, ""),
                                                                   ([], ""),
                                                                   ([""], "")])
def test_parse_description(raw_description, expected_description):
    assert parse_description(raw_description) == expected_description


@pytest.mark.parametrize("raw_format, expected_format", [(['application/pdf'], "PDF"),
                                                         (['application/epub+zip'], "EPUB"),
                                                         (['video/mp4'], ""),
                                                         ("application/pdf", ""),
                                                         (None, ""),
                                                         ([""], "")])
def test_parse_format(raw_format, expected_format):
    assert parse_format(raw_format) == expected_format


@pytest.mark.parametrize("raw_identifier, expected_isbn",
                         [(['https://openresearchlibrary.org/viewer/9fa24158-ec43-4b6f-9c99-f8edd0e5b260',
                            'https://openresearchlibrary.org/ext/api/media/9fa24158-ec43-4b6f-9c99-f8edd0e5b260/assets/external_content.pdf',
                            'ISBN:9780199660797',
                            'DOI:https://dx.doi.org/10.1093/acprof:oso/9780199660797.001.0001'], "9780199660797"),
                          (['https://openresearchlibrary.org/viewer/9fa24158-ec43-4b6f-9c99-f8edd0e5b260',
                            'https://openresearchlibrary.org/ext/api/media/9fa24158-ec43-4b6f-9c99-f8edd0e5b260/assets/external_content.pdf',
                            'DOI:https://dx.doi.org/10.1093/acprof:oso/9780199660797.001.0001'], "")])
def test_parse_isbn(raw_identifier, expected_isbn):
    assert parse_isbn(raw_identifier) == expected_isbn


@pytest.mark.parametrize("raw_identifier, expected_link", [
    (["https://openresearchlibrary.org/ext/api/media/8b3ffc67-6ff8-4a25-8a02-f7241dc31fec/assets/external_content.pdf"],
     "https://openresearchlibrary.org/ext/api/media/8b3ffc67-6ff8-4a25-8a02-f7241dc31fec/assets/external_content.pdf"),
    (["https://openresearchlibrary.org/viewer/90626a3e-7088-41c2-ba48-92bb633b1cb7"],
     "https://openresearchlibrary.org/ext/api/media/90626a3e-7088-41c2-ba48-92bb633b1cb7/assets/external_content.pdf"),
    (['no_link_here', 'and_no_link_here'], ""),
    ([], ""),
    (None, "")
])
def test_parse_download_link(raw_identifier, expected_link):
    assert parse_download_link(raw_identifier) == expected_link


@pytest.mark.parametrize("raw_language, expected_code", [(['English'], "1"),
                                                         (['German'], "2"),
                                                         (['NotExist'], ""),
                                                         (None, ""),
                                                         ([], "")])
def test_parse_language(raw_language, expected_code):
    assert parse_language(raw_language) == expected_code


@pytest.mark.parametrize("raw_publisher, expected_publisher", [(['Oxford University Press'], "Oxford University Press"),
                                                               (['OUP', 'OOO'], "OUP"),
                                                               ([''], ""),
                                                               (None, ""),
                                                               ([], "")])
def test_parse_publisher(raw_publisher, expected_publisher):
    assert parse_publisher(raw_publisher) == expected_publisher


@pytest.mark.parametrize("raw_subject, expected_bisacs", [(['History / Military / World War Ii',
                                                            'bisacsh:HIS027100',
                                                            'History / Europe',
                                                            'bisacsh:HIS010000',
                                                            'History / Modern / 20th Century',
                                                            'bisacsh:HIS037070'], ['HIS027100', 'HIS010000', 'HIS037070']),
                                                          (['History / Military / World War Ii',
                                                            'History / Europe',
                                                            'History / Modern / 20th Century'], []),
                                                          ([''], []),
                                                          (None, []),
                                                          ([], [])])
def test_parse_subject(raw_subject, expected_bisacs):
    assert parse_subject(raw_subject) == expected_bisacs


@pytest.mark.parametrize("raw_title, expected_title", [(['I am title'], 'I am title'),
                                                          ([''], ""),
                                                          (None, ""),
                                                          ([], "")])
def test_parse_title(raw_title, expected_title):
    assert parse_title(raw_title) == expected_title
