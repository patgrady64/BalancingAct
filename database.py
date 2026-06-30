import sqlite3

def init_db():
    """Initializes the database and creates the transactions table."""
    conn = sqlite3.connect("balancing_act.db")
    cursor = conn.cursor()
    
    # We store the scenario prompt text and the correct debit/credit answers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS current_scenario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            account TEXT NOT NULL,
            type TEXT NOT NULL, -- 'DEBIT' or 'CREDIT'
            amount REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_scenario(transactions):
    """Clears the old practice session and saves the new one.
    Expects a list of dicts: [{'prompt': ..., 'account': ..., 'type': ..., 'amount': ...}]
    """
    conn = sqlite3.connect("balancing_act.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM current_scenario") # Wipe previous run
    
    for tx in transactions:
        cursor.execute("""
            INSERT INTO current_scenario (prompt, account, type, amount)
            VALUES (?, ?, ?, ?)
        """, (tx['prompt'], tx['account'], tx['type'], tx['amount']))
        
    conn.commit()
    conn.close()

def get_answer_key():
    """Fetches the correct balances aggregated by account for the 'Check' button."""
    conn = sqlite3.connect("balancing_act.db")
    cursor = conn.cursor()
    
    # Simple math: For Cash/AR, Debits increase, Credits decrease.
    # For Equity/Revenue, Credits increase, Debits decrease.
    cursor.execute("SELECT account, type, amount FROM current_scenario")
    rows = cursor.fetchall()
    conn.close()
    
    balances = {
        "Cash": 0.0,
        "Accounts Receivable": 0.0,
        "Owner's Equity": 0.0,
        "Sales Revenue": 0.0
    }
    
    for account, tx_type, amount in rows:
        if account in ["Cash", "Accounts Receivable"]:
            balances[account] += amount if tx_type == "DEBIT" else -amount
        elif account in ["Owner's Equity", "Sales Revenue"]:
            balances[account] += amount if tx_type == "CREDIT" else -amount
            
    return balances