from typing import Dict
from ..cashflows.amortization import loan_amortization
from .handlers import tranche_handler, reserve_handler

NODE_REGISTRY = {
    "tranche": tranche_handler,
    "reserve": reserve_handler
}

def initialize_state_from_deal(deal_json: Dict) -> Dict:
    # simple state initialization
    n_periods = deal_json.get("n_periods", 360)
    state = {
        "period": 0,
        "n_periods": n_periods,
        "tranche_balances": {},
        "reserve_accounts": {},
        "allocations": {},
        "results": {}
    }

    # seed tranche balances
    for node in deal_json.get("waterfall", []):
        node_type = node.get("type")
        params = node.get("params", {})
        if node_type == "tranche":
            name = params.get("name") or node.get("id")
            balance = params.get("balance", 0.0)
            state["tranche_balances"][name] = balance
        elif node_type == "reserve":
            name = params.get("name") or node.get("id")
            starting_balance = params.get("starting_balance", 0.0)
            state["reserve_accounts"][name] = starting_balance

    return state

def apply_waterfall(deal_json: Dict) -> Dict:
    state = initialize_state_from_deal(deal_json)
    results = []

    pool_balance = sum(l.get("balance", 0.0) for l in deal_json.get("pool", {}).get("loans", []))
    coupon = deal_json.get("pool", {}).get("coupon", 0.05)

    for period in range(deal_json.get("n_periods", 360) + 1):
        state["period"] = period
        # naive pool cashflow: interest = coupon * pool_balance / 12, principal = amortization slice
        interest = pool_balance * coupon / 12.0
        principal = 0.0
        # simple amortization: if scheduled principal exists, remove a fixed chunk towards final
        scheduled = deal_json.get("pool", {}).get("scheduled_principal", [])
        if scheduled:
            principal = min(pool_balance, scheduled)
        # otherwise assume no scheduled amortization; use zero

        state["available_interest"] = interest
        state["available_principal"] = principal

        for node in deal_json.get("waterfall", []):
            handler = NODE_REGISTRY.get(node.get("type"))
            if handler is None:
                raise Exception(f"Unknown node type: {node.get('type')}")
            state = handler(node, state)

        # record results for the period
        results.append({
            "period": period,
            "available_interest": interest,
            "available_principal": principal,
            "allocations": state["allocations"].get(period, [])
        })

        # reduce pool_balance by principal
        pool_balance = max(0.0, pool_balance - principal)

    state["results"] = results

    return state