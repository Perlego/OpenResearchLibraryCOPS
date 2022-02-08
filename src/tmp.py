import ast
from pprint import pprint

from src.contants import PROCESSED_IDS
from src.fields_parser import parse_isbn, parse_language
from src.utils import execute_select, execute_insert_or_update
from config import HOST_URL, USERNAME, PASSWORD, DB_NAME

if __name__ == '__main__':
    connection_details = dict(
        host=HOST_URL,
        username=USERNAME,
        password=PASSWORD,
        dbname=DB_NAME,
    )

    with open("/home/aviaowl/PycharmProjects/OpenResearchLibraryCOPS/src/output_right.csv") as output:
        lines = output.readlines()
    originals = dict()
    for line in lines:
        line = line.strip()
        record = ast.literal_eval(line)
        isbn = parse_isbn(record["identifier"])
        language = parse_language(record["language"])
        originals[isbn] = {'language': language}

    ids = ','.join(str(idd) for idd in PROCESSED_IDS)
    query = f"SELECT id, language_id, ProductIdentifier_ISBN13_IDValue from meta_data where id in ({ids})"
    rows = execute_select(query, connection_details)

    query = f"SELECT id, language from languages"
    languages = execute_select(query, connection_details)
    lang_dict = {row['language']: row['id'] for row in languages}

    i = 0
    for row in rows:
        isbn = row['ProductIdentifier_ISBN13_IDValue']
        # print(f"isbn: {isbn}, old_language: {row['language_id']}, new language: {}")
        query = f"update meta_data set language_id={lang_dict[originals[isbn]['language']]} where id={row['id']}"
        print(execute_insert_or_update(query, connection_details))