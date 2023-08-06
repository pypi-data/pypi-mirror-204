from datetime import date
from io import StringIO

from ledes_parser.ledes_1998B_parser import Ledes1998BParser

VALID_1998B_DATA = """LEDES1998B[]
INVOICE_DATE|INVOICE_NUMBER|CLIENT_ID|LAW_FIRM_MATTER_ID|INVOICE_TOTAL|BILLING_START_DATE|BILLING_END_DATE|INVOICE_DESCRIPTION|LINE_ITEM_NUMBER|EXP/FEE/INV_ADJ_TYPE|LINE_ITEM_NUMBER_OF_UNITS|LINE_ITEM_ADJUSTMENT_AMOUNT|LINE_ITEM_TOTAL|LINE_ITEM_DATE|LINE_ITEM_TASK_CODE|LINE_ITEM_EXPENSE_CODE|LINE_ITEM_ACTIVITY_CODE|TIMEKEEPER_ID|LINE_ITEM_DESCRIPTION|LAW_FIRM_ID|LINE_ITEM_UNIT_COST|TIMEKEEPER_NAME|TIMEKEEPER_CLASSIFICATION|CLIENT_MATTER_ID[]
19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|1|F|2.00|-70|630|19990115|L510||A102|22547|Research Attorney’s fees, Set off claim|24-6437381|350|Arnsley, Robert|PARTNR|423-987[]
19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|2|F|2.00|0|700|19990115|L510||A102|22547|Research attorney's fees, Trial pleading|24-6437381|350|Arnsley, Robert|PARTNR|423-987[]
19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|3|F|0.200|0|40|19990116|L510||A107|45875|Telephone conference with John Doe|24-6437381|200|Beaster, John|ASSOC|423-987[]
19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|4|E|1|0|24.95|19990117||E111|||Meals|24-6437381|24.95|||423-987[]
19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|5|E|1|0|289.5|19990117||E110|||Out-of_town travel|24-6437381|289.5|||423-987[]
19990225|96543|00711|1326|1250|19990101|19990131|Monthly Retainer|6|IF|1|1250.|1250|19990131|||||Monthly Retainer Fee|24-6437381||||425-936[]
"""


def test_ledes1998B_parse_textio():
    parser = Ledes1998BParser()
    invoices = parser.parse(StringIO(VALID_1998B_DATA, newline='\n'))

    assert len(invoices) > 0


def test_ledes1998B_parser_should_parse_file():
    parser = Ledes1998BParser()
    with open(file="tests/ledes_98B_sample_file.txt", mode="r") as f:
        invoices = parser.parse(f)

    assert len(invoices) > 0


def test_ledes1998B_parser_should_parse_invoice_date():
    parser = Ledes1998BParser()
    invoices = parser.parse(StringIO(VALID_1998B_DATA))

    first_invoice = invoices[0]
    invoice_date = first_invoice.invoice_date
    assert isinstance(first_invoice.invoice_date, date)
    assert invoice_date.year == 1999
    assert invoice_date.month == 2
    assert invoice_date.day == 25


def test_ledes1998B_parser_should_parse_invoice_number():
    parser = Ledes1998BParser()
    invoices = parser.parse(StringIO(VALID_1998B_DATA))

    first_invoice = invoices[0]
    invoice_number = first_invoice.invoice_number
    assert invoice_number is not None


def test_ledes1998B_parser_should_parse_client_id():
    parser = Ledes1998BParser()
    invoices = parser.parse(StringIO(VALID_1998B_DATA))

    first_invoice = invoices[0]
    client_id = first_invoice.client_id
    assert client_id is not None


def test_ledes1998B_parser_should_parse_law_firm_matter_id():
    parser = Ledes1998BParser()
    invoices = parser.parse(StringIO(VALID_1998B_DATA))

    first_invoice = invoices[0]
    law_firm_matter_id = first_invoice.law_firm_matter_id
    assert law_firm_matter_id is not None
