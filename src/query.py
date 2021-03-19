import ast

from src.fields_parser import parse_isbn

if __name__ == "__main__":
    with open("/home/aviaowl/PycharmProjects/OpenResearchLibraryCOPS/src/output_right.csv") as output:
        lines = output.readlines()
    unique_rights = []
    connection_details = dict(host="", username="", password="", dbname="")
    cc_by = "https://creativecommons.org/licenses/by/4.0/legalcode"
    public_domain = "https://wiki.creativecommons.org/wiki/public_domain"
    knowledge_unlatched = "MODID-00000000488:Knowledge Unlatched"
    with open("/home/aviaowl/PycharmProjects/OpenResearchLibraryCOPS/src/output_final.csv", "a") as final:
        j = 0
        for line in lines:
            line = line.strip()
            isbns_list = []
            record = ast.literal_eval(line)
            if record["type"][0] == "BOOK" and (
                public_domain in record["rights"]
                or cc_by in record["rights"]
                or knowledge_unlatched in record["source"]
            ):
                isbn = parse_isbn(record["identifier"])
                final.write(f"{record}\n")
