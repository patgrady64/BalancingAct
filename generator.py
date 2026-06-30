import random
from database import save_scenario

def generate_new_demo():
    """Generates a random set of business events, flattens them into journal entries,
    saves them to the DB, and returns the plain text prompts for the UI.
    """
    pool_of_events = [
        "investment", "cash_sale", "credit_sale", "collection"
    ]
    
    # Select 4 to 6 random events to build a 'period'
    selected_events = random.choices(pool_of_events, k=random.randint(4, 6))
    
    prompts = []
    all_journal_entries = []
    
    for event in selected_events:
        amount = float(random.randint(5, 150) * 100) # Generates clean amounts like $1,200, $8,500
        
        if event == "investment":
            text = f"Owner invests ${amount:,.2f} cash into the business."
            entries = [
                {"account": "Cash", "type": "DEBIT", "amount": amount},
                {"account": "Owner's Equity", "type": "CREDIT", "amount": amount}
            ]
        elif event == "cash_sale":
            text = f"Performed services and received ${amount:,.2f} cash immediately."
            entries = [
                {"account": "Cash", "type": "DEBIT", "amount": amount},
                {"account": "Sales Revenue", "type": "CREDIT", "amount": amount}
            ]
        elif event == "credit_sale":
            text = f"Billed a customer ${amount:,.2f} for services completed on account."
            entries = [
                {"account": "Accounts Receivable", "type": "DEBIT", "amount": amount},
                {"account": "Sales Revenue", "type": "CREDIT", "amount": amount}
            ]
        elif event == "collection":
            text = f"Collected ${amount:,.2f} cash from a customer on an outstanding invoice."
            entries = [
                {"account": "Cash", "type": "DEBIT", "amount": amount},
                {"account": "Accounts Receivable", "type": "CREDIT", "amount": amount}
            ]
            
        prompts.append(text)
        for entry in entries:
            all_journal_entries.append({
                "prompt": text,
                "account": entry["account"],
                "type": entry["type"],
                "amount": entry["amount"]
            })
            
    # Save the absolute truth to SQLite
    save_scenario(all_journal_entries)
    
    # Return unique bulleted list of things the user has to log
    return prompts