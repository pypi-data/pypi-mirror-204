from abc import ABC, abstractmethod
from typing import Iterable, List

from .typings.invoice_types import Invoice


class BaseLedesParser(ABC):
    @abstractmethod
    def parse(self, csv_data: Iterable[str]) -> List[Invoice]:
        pass
