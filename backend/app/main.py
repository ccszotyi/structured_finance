from fastapi import UploadFile, File
import pandas as pd
import io

@app.post("/upload/loans")
def upload_loans(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        return {"error": "Please upload a CSV file."}
    
    content = file.file.read().decode('utf-8')
    df = pd.read_csv(io.BytesIO(content))

    required_columns = {"loan_id", "balance", "coupon", "term_months"}
    if not required_columns.issubset(df.columns):
        return {"error": f"CSV must contain columns: {required_columns}"}
    
    loans = df.to_dict(orient='records')
    return {"loans": loans}

@app.get("/node_schemas")
def node_schemas():
    return {
        "tranche_interest": {
            "label": "Tranche Interest",
            "params": ["name", "balance", "coupon"]
        },
        "tranche_principal": {
            "label": "Tranche Principal",
            "params": ["name"]
        },
        "reserve": {
            "label": "Reserve Account",
            "params": ["target_balance", "min_balance", "sweep_priority"]
        }
    }