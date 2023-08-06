from csv import reader
from typing import Iterable, List

from ledes_parser.base_ledes_parser import BaseLedesParser

from .typings.invoice_types import Invoice


class Ledes1998BIParser(BaseLedesParser):
    def parse(self, csv_data: Iterable[str]) -> List[Invoice]:
        invoices = []
        csv_reader = reader(csv_data, delimiter="|")

        for row in csv_reader:
            pass
            # Parse fields according to the 1998BI format
            # ...
        return invoices
