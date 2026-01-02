from typing import List

from .loan import Loan

class Pool:
    def __init__(self, loans: List[Loan]):
        self.loans = loans

    def total_balance(self) -> float:
        return sum(l.balance for l in self.loans)

    def copy(self) -> "Pool":
        return Pool([l.copy() for l in self.loans])