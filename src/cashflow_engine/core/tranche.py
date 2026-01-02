from dataclasses import dataclass

@dataclass
class Tranche:
    name: str
    balance: float
    coupon: float
    seniority: int # 0 = most senior

    def copy(self) -> "Tranche":
        return Tranche(
            name=self.name,
            balance=self.balance,
            coupon=self.coupon,
            seniority=self.seniority
        )