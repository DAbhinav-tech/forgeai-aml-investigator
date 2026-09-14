from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI(title="Bank Ledger API")

def get_db_connection(bank_name):
    if bank_name not in ["bank_a", "bank_b"]:
        raise HTTPException(status_code=400, detail="Invalid bank name. Use 'bank_a' or 'bank_b'.")
    conn = sqlite3.connect(f"{bank_name}.db")
    # This allows column access by name
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/{bank_name}/transactions")
def get_all_transactions(bank_name: str, limit: int = 50):
    """Endpoint for the Monitor Agent to fetch recent transaction batches."""
    conn = get_db_connection(bank_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/{bank_name}/transaction/{tx_id}")
def get_transaction(bank_name: str, tx_id: str):
    """Endpoint for the Investigator Agent to fetch specific flagged transactions."""
    conn = get_db_connection(bank_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE tx_id = ?", (tx_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return dict(row)