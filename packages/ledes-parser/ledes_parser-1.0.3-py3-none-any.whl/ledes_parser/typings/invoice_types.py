from datetime import date
from typing import List


class LineItem():
    line_item_number: str
    exp_fee_inv_adj_type: str
    adjustment_amount: float
    number_of_units: float
    unit_cost: float
    line_item_total: float
    line_item_date: date
    task_code: str
    expense_code: str
    activity_code: str
    timekeeper_id: str
    timekeeper_name: str
    timekeeper_classification: str
    description: str
    law_firm_id: str


class Invoice():
    invoice_number: str
    client_id: str
    client_matter_id: str
    invoice_date: date
    invoice_description: str
    invoice_total: float
    line_items: List[LineItem]
    law_firm_matter_id: str
    billing_start_date: date
    billing_end_date: date

    def __init__(self) -> None:
        self.line_items = list()

    def add_line_item(self, line_item: LineItem) -> None:
      # TODO: Validation that there aren't duplicate line item numbers.
      self.line_items.append(line_item)
