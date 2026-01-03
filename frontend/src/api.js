const API = "http://localhost:8000";

export async function getNodeSchemas() {
    const r = await fetch(`${API}/node_schemas/`);
    return await r.json();
}

export async function uploadLoans(file) {
    const form = new FormData();
    form.append("file", file);

    const r = await fetch(`${API}/upload_loans/`, {
        method: "POST",
        body: form,
    });
    return await r.json();
}

export async function patchDeal(dealId, data) {
    await fetch(`${API}/deals/${dealId}/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
}

export async function runDeal(dealId) {
    const r = await fetch(`${API}/deals/${dealId}/run/`, {
        method: "POST",
    });
    return r.json()
}