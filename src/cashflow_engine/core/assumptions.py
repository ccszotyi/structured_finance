from dataclasses import dataclass

@dataclass
class Assumptions:
    cpr: float = 0.0
    default_rate: float = 0.0
    recovery_rate: float = 0.0