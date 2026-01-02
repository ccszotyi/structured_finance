from dataclasses import dataclass

@dataclass
class Loan:
    loan_id: str
    balance: float
    coupon: float
    term_months: int
    
    def copy(self) -> "Loan":
        return Loan(
            loan_id=self.loan_id,
            balance=self.balance,
            coupon=self.coupon,
            term_months=self.term_months
        )
    