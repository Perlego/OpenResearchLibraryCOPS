import pytest

from src.utils import generate_product_reference, get_contributors_dict


@pytest.mark.parametrize(
    "extension, isbn, expected_product_reference",
    [
        ("PDF", "9780199660797", "9780199660797.pdf"),
        ("epub", "9780199660797", "9780199660797.epub"),
        ("jpg", "9780199660797", ""),
        ("epub", "", ""),
    ],
)
def test_generate_product_reference(isbn, extension, expected_product_reference):
    assert generate_product_reference(extension, isbn) == expected_product_reference


def test_get_contributors_dict():
    contributors = (
        "Daenerys Stormborn of the House Targaryen,First of Her Name, "
        "the Unburnt, "
        "Queen of the Andals and the First Men, "
        "Khaleesi of the Great Grass Sea,"
        "Breaker of Chains, "
        "and Mother of Dragons"
    )
    expected_dict = dict(
        contributor_role="A01", person_name=contributors, sequence_number="1"
    )
    assert get_contributors_dict(contributors) == expected_dict
