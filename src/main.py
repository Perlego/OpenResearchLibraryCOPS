from pprint import pprint

from sickle import Sickle
from sickle.models import Record

if __name__ == '__main__':
    sickle = Sickle('https://catalog.openresearchlibrary.org/oai')
    records = sickle.ListRecords(metadataPrefix='oai_dc')
    for _ in range(1):
        first_record: Record = records.next()
        pprint(first_record.metadata)

