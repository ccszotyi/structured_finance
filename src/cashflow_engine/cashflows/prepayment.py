def cpr_to_smm(cpr: float, freq: int=12) -> float:
    """
    Convert Conditional Prepayment Rate (CPR) to Single Monthly Mortality (SMM).

    Args:
        cpr (float): The annual CPR rate (between 0 and 1).
        freq (int): The number of payment periods in a year. Default is 12 for monthly.

    Returns:
        float: The equivalent SMM rate (between 0 and 1).
    """
    if not (0 <= cpr <= 1):
        raise ValueError("CPR must be between 0 and 1.")
    if freq <= 0:
        raise ValueError("Frequency must be a positive integer.")

    smm = 1 - (1 - cpr) ** (1 / freq)
    return smm