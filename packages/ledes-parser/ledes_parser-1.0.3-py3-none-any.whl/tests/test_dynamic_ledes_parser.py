
# import csv
# from datetime import date

# from ledes_parser.ledes_dynamic_parser import DynamicLEDESParser


# def test_dynamic_parser():
#     parser = DynamicLEDESParser(format_file='ledes_parser/ledes_1998_specification.json')
#     with open('tests/sample_data.txt', 'r') as f:
#         reader = csv.reader(f, delimiter="|")
#         invoices = parser.parse(reader)

#     assert len(invoices) > 0


# def test_dynamic_parser_should_parse_invoice_date():
#     parser = DynamicLEDESParser(format_file='ledes_parser/ledes_1998_specification.json')
#     with open('tests/sample_data.txt', 'r') as f:
#         reader = csv.reader(f, delimiter="|")
#         invoices = parser.parse(reader)

#     first_invoice = invoices[0]
#     invoice_date = first_invoice.invoice_date
#     assert isinstance(first_invoice.invoice_date, date)
#     assert invoice_date.year == 1999
#     assert invoice_date.month == 2
#     assert invoice_date.day == 25
