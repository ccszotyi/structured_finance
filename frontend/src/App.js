import React, { useState } from 'react';
import WaterfallEditor from './components/WaterfallEditor';
import LoanUploader from './components/LoanUploader';

export default function App() {
    const [deal, setDeal] = useState({
        deal_id: "local-deal",
        n_periods: 12,
        pool: {loans: [], coupon: 0.05},
        waterfall: [
            {
                id: "A_int",
                type: "tranche_interest",
                params: { name:"A", balance: 70000, coupon: 0.03 }
            },
            {
                id: "A_prin",
                type: "tranche_principal",
                params: { name:"A" }
            },
        ]
    })

    return (
        <div style={{ padding: 20 }}>
            <h1>Cashflow Engine UI (MVP)</h1>
            <LoanUploader deal={deal} setDeal={setDeal} />
            <WaterfallEditor deal={deal} setDeal={setDeal} />
        </div>
  );
}
