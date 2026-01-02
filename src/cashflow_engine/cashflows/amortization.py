import pandas as pd
from .prepayment import cpr_to_smm

def loan_amortization(
        balance: float,
        annual_coupon: float,
        term_months: int,
        cpr: float = 0.0
):
    monthly_rate = annual_coupon / 12
    smm = cpr_to_smm(cpr)

    if monthly_rate == 0:
        monthly_payment = balance / term_months
    else:
        monthly_payment = balance * monthly_rate / (1 - (1 + monthly_rate) ** - term_months)

    rows = []
    bal = balance
    for period in range(1, term_months + 1):
        interest = bal * monthly_rate
        scheduled_principal = max(0.0, monthly_payment - interest)
        prepayment = max(0.0, (bal - scheduled_principal) * smm)
        total_principal = min(bal, scheduled_principal + prepayment)
        bal -= total_principal

        rows.append({
            "Period": period,
            "Beginning Balance": bal + total_principal,
            "Scheduled Payment": monthly_payment,
            "Interest": interest,
            "Scheduled Principal": scheduled_principal,
            "Prepayment": prepayment,
            "Total Principal": total_principal,
            "Ending Balance": bal
        })
        if bal <= 1e-8:
            break
    
    return pd.DataFrame(rows)