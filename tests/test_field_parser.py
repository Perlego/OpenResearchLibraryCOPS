import pytest

from src.fields_parser import parse_creator, parse_date


@pytest.mark.parametrize("raw_creator, expected_creator", [(['Potter, Harry'], "Harry Potter"),
                                                           (['Granger, Hermione', 'Potter, Harry'], "Hermione Granger, Harry Potter"),
                                                           (['Granger, Hermione', 'Potter, Harry', ''], "Hermione Granger, Harry Potter"),
                                                           (['Hermione Granger', 'Harry Potter'], "Hermione Granger, Harry Potter"),
                                                           ([None, 1234, 'Harry Potter'], "Harry Potter"),
                                                           ("Ron Weasley", "",)])
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



def test_parse_description(raw_description, expected_description):
    assert raw_description==expected_description