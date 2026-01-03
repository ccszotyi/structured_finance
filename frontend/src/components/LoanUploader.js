import React from "react";
import { uploadLoans } from "../api";

export default function LoanUploader({ deal, setDeal}) {
    async function handleUpload(e) {
        const file = e.target.files[0];
        if (!file) return;

        const res = await uploadLoans(file);
        setDeal({
            ...deal,
            pool: { ...deal.pool, loans: res.loans },
        });
    }

    return (
        <div>
            <h3>Upload Loans (CSV)</h3>
            <input type="file" accept=".csv" onChange={handleUpload} />
        </div>
    );
}