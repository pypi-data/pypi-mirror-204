from datetime import datetime
from enum import IntEnum
import logging
from typing import Iterable, List

from ledes_parser.base_ledes_parser import BaseLedesParser

from .typings.invoice_types import Invoice, LineItem
from csv import reader

class Position(IntEnum):
    INVOICE_DATE = 0
    INVOICE_NUMBER = 1
    CLIENT_ID = 2
    LAW_FIRM_MATTER_id = 3
    INVOICE_TOTAL = 4
    BILLING_START_DATE = 5
    BILLING_END_DATE = 6
    INVOICE_DESCRIPTION = 7
    LINE_ITEM_NUMBER = 8
    EXP_FEE_INV_ADJ_TYPE = 9
    NUMBER_OF_UNITS = 10
    ADJUSTMENT_AMOUNT = 11
    LINE_ITEM_TOTAL = 12
    LINE_ITEM_DATE = 13
    TASK_CODE = 14
    EXPENSE_CODE = 15
    ACTIVITY_CODE = 16
    TIMEKEEPER_ID = 17
    DESCRIPTION = 18
    LAW_FIRM_ID = 19
    UNIT_COST = 20
    TIMEKEEPER_NAME = 21
    TIMEKEEPER_CLASSIFICATION = 22
    CLIENT_MATTER_ID = 23
    

class Ledes1998BParser(BaseLedesParser):
    def parse(self, csv_data: Iterable[str]) -> List[Invoice]:
        invoices = []
        csv_reader = reader(csv_data, delimiter="|")

        # First line contains the ledes format.
        next(csv_reader)

        # Second line contains the column headers.
        next(csv_reader)

        row_number = 2 # Where the first record is
        for row in csv_reader:
            row_number += 1
            # Parse invoice according to https://ledes.org/ledes-98b-format/#
            if not row:
                continue

            current_invoice = Invoice()

            current_invoice.invoice_number = row[Position.INVOICE_NUMBER]
            logging.debug(f"Parsing invoice number '{row[1]}' on row {row_number}.")

            current_invoice.invoice_date = datetime.strptime(row[Position.INVOICE_DATE], "%Y%m%d")
            current_invoice.client_id = row[Position.CLIENT_ID]
            current_invoice.law_firm_matter_id = row[Position.LAW_FIRM_MATTER_id]
            current_invoice.invoice_total = row[Position.INVOICE_TOTAL]
            current_invoice.billing_start_date = datetime.strptime(row[Position.BILLING_START_DATE], "%Y%m%d")
            current_invoice.billing_end_date = datetime.strptime(row[Position.BILLING_END_DATE], "%Y%m%d")
            current_invoice.invoice_description = row[Position.INVOICE_DESCRIPTION]
            current_invoice.client_matter_id = row[Position.CLIENT_MATTER_ID]

            current_line_item = LineItem()
            current_line_item.line_item_number = row[Position.LINE_ITEM_NUMBER]
            current_line_item.exp_fee_inv_adj_type = row[Position.EXP_FEE_INV_ADJ_TYPE]
            current_line_item.number_of_units = row[Position.NUMBER_OF_UNITS]
            current_line_item.adjustment_amount = 0 if row[Position.ADJUSTMENT_AMOUNT] == '' else float(row[Position.ADJUSTMENT_AMOUNT])
            current_line_item.line_item_total = float(row[Position.LINE_ITEM_TOTAL])
            current_line_item.line_item_date = datetime.strptime(row[Position.LINE_ITEM_DATE], "%Y%m%d")
            current_line_item.task_code = row[Position.TASK_CODE]
            current_line_item.expense_code = row[Position.EXPENSE_CODE]
            current_line_item.activity_code = row[Position.ACTIVITY_CODE]
            current_line_item.timekeeper_id = row[Position.TIMEKEEPER_ID]
            current_line_item.description = row[Position.DESCRIPTION]
            current_line_item.law_firm_id = row[Position.LAW_FIRM_ID]
            current_line_item.unit_cost = 0 if row[Position.UNIT_COST] == '' else float(row[Position.UNIT_COST])
            current_line_item.timekeeper_name = row[Position.TIMEKEEPER_NAME]
            current_line_item.timekeeper_classification = row[Position.TIMEKEEPER_CLASSIFICATION]

            current_invoice.line_items.append(current_line_item)

            invoices.append(current_invoice)

        return invoices
