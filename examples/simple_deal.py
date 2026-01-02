import pandas as pd
from cashflow_engine.waterfall.engine import apply_waterfall

example = {
    "deal_id": "example-deal",
    "n_periods": 6,
    "pool": {
        "loans": [
            {"loan_id": "L1", "balance": 100000, "coupon": 0.05, "term_months": 360}
        ],
        "coupon": 0.05,
        "scheduled_principal": 10000,
    },
    "waterfall": [
        {
            "id": "n1",
            "type": "tranche",
            "params": {"name": "Senior", "balance": 70000, "coupon": 0.03},
        },
        {
            "id": "n2",
            "type": "reserve",
            "params": {
                "target_balance": 5000,
                "min_balance": 0,
                "sweep_priority": "principal",
            },
        },
    ],
}

out = apply_waterfall(example)

# print(out["results"])

period_rows = []
for p in out["results"]:
    row = {
        "period": p["period"]
    }
    for alloc in p["allocations"]:
        node_name = alloc.get("name") or alloc.get("node_id")
        node_type = alloc.get("node_type")

        col_name = f"{node_type}_{node_name}_EoP"
        row[col_name] = alloc["ending_balance"]
    period_rows.append(row)

df = pd.DataFrame(period_rows)

print(df)

