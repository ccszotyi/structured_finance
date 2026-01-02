from typing import List, Dict

from .assumptions import Assumptions
from .pool import Pool
from .tranche import Tranche

class Deal:
    def __init__(self, deal_json: Dict):
        self.deal_json = deal_json

    def get_waterfall(self):
        return self.deal_json.get("waterfall", [])
    
    def get_pool(self) -> Pool:
        loans = []
        for l in self.deal_json.get("pool", {}).get("loans", []):
            loans.append(
                # lazy import to avoid circular dependency
                __import__("cashflow_engine.core.loan", fromlist=["Loan"]).Loan(
                    loan_id=l["loan_id"],
                    balance=l["balance"],
                    coupon=l["coupon"],
                    term_months=l["term_months"]
                )
            )