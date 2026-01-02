from typing import Dict

def tranche_handler(
        node: Dict,
        state: Dict
) -> Dict:
    """
    Handles the processing of a tranche node in the cashflow waterfall.

    Args:
        node (Dict): The tranche node containing its properties.
        state (Dict): The current state of the cashflow processing.

    Returns:
        Dict: Updated state after processing the tranche node.
    """
    params = node.get("params", {})
    name = params.get("name") or node.get("id")
    coupon = params.get("coupon", 0.0)

    # interest due monthly
    period_rate = coupon / 12.0
    balance = state["tranche_balances"].get(name, params.get("balance", 0.0))
    interest_due = balance * period_rate
    interest_paid = min(interest_due, state["available_interest"])
    state["available_interest"] -= interest_paid

    # principal allocation
    principal_paid = min(balance, state["available_principal"])
    state["available_principal"] -= principal_paid
    balance -= principal_paid

    # update tranche balance
    state["tranche_balances"][name] = balance
    state["allocations"].setdefault(state["period"], []).append({
        "node_id": node["id"],
        "node_type": "tranche",
        "name": name,
        "interest_due": interest_due,
        "interest_paid": interest_paid,
        "principal_paid": principal_paid,
        "ending_balance": balance
    })

    return state

def reserve_handler(
        node: Dict,
        state: Dict
) -> Dict:
    """
    Handles the processing of a reserve node in the cashflow waterfall.

    Args:
        node (Dict): The reserve node containing its properties.
        state (Dict): The current state of the cashflow processing.

    Returns:
        Dict: Updated state after processing the reserve node.
    """
    params = node.get("params", {})
    name = params.get("name") or node.get("id")
    min_balance = params.get("min_balance", 0.0)
    target_balance = params.get("target_balance", 0.0)
    current_balance = state["reserve_balances"].get(name, 0.0)

    shortfall = max(0.0, target_balance - current_balance)

    sweep_priority = params.get("sweep_priority", "principal")

    funding_total = 0.0
    if shortfall > 0:
        # Need to fund the reserve
        if sweep_priority == "principal":
            funding = min(shortfall, state["available_principal"])
            state["available_principal"] -= funding
            current_balance += funding
            shortfall -= funding
            funding_total += funding
            if shortfall > 0:
                funding = min(shortfall, state["available_interest"])
                state["available_interest"] -= funding
                current_balance += funding
                funding_total += funding
        elif sweep_priority == "interest":
            funding = min(shortfall, state["available_interest"])
            state["available_interest"] -= funding
            current_balance += funding
            shortfall -= funding
            funding_total += funding
            if shortfall > 0:
                funding = min(shortfall, state["available_principal"])
                state["available_principal"] -= funding
                current_balance += funding
                funding_total += funding
    else:
        # Excess funds can be released
        release = min(-shortfall, current_balance)
        current_balance -= release
        state["available_principal"] += release

    # update reserve balance
    state["reserve_balances"][name] = current_balance
    state["allocations"].setdefault(state["period"], []).append({
        "node_id": name,
        "node_type": "reserve",
        "funding_total": funding_total,
        "ending_balance": current_balance
    })

    return state