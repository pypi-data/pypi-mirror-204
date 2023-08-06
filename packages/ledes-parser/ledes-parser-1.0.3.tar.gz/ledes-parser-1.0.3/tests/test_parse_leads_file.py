from ledes_parser import parse_ledes_file


def test_parse_ledes_file_with_file_path_should_succeed():
    with open('tests/ledes_98B_sample_file.txt', 'r') as f:
        invoices = parse_ledes_file(f, "1998B")

    assert len(invoices) > 0
