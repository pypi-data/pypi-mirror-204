from csv import reader
from typing import Iterable, List, TextIO

from ledes_parser.base_ledes_parser import BaseLedesParser

from .typings.invoice_types import Invoice


class Ledes1998BIV2Parser(BaseLedesParser):
    def parse(self, csv_data: Iterable[str]) -> List[Invoice]:
        invoices = []
        csv_reader = reader(csv_data, delimiter="|")

        # First line contains the ledes format.
        next(csv_reader)

        # Second line contains the column headers.
        next(csv_reader)

        for row in csv_reader:
            pass
            # Parse fields according to the 1998BIV2 format
            # ...
        return invoices
