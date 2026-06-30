import random
from database import save_scenario

def generate_new_demo(difficulty="Easy"):
    """Generates a dynamic period of business events based on chosen difficulty.
    Supported modes: 'Easy', 'Medium', 'Hard', 'Hardest'
    """
    pool_of_events = ["investment", "cash_sale", "credit_sale", "collection"]
    
    # Configure parameters based on difficulty scale
    if difficulty == "Easy":
        num_transactions = random.randint(3, 4)
        use_decimals = False
        amount_range = (10, 50)  # Simple values like $1,000 - $5,000
    elif difficulty == "Medium":
        num_transactions = random.randint(6, 8)
        use_decimals = False
        amount_range = (50, 150) # Values like $5,000 - $15,000
    elif difficulty == "Hard":
        num_transactions = random.randint(10, 12)
        use_decimals = True
        amount_range = (5, 120)  # Messy real-world scale
    else:  # Hardest
        num_transactions = random.randint(15, 20)
        use_decimals = True
        amount_range = (1, 200)  # High volume, complex numbers
        
    selected_events = random.choices(pool_of_events, k=num_transactions)
    
    prompts = []
    all_journal_entries = []
    
    for i, event in enumerate(selected_events, 1):
        # Determine the number value format
        if use_decimals:
            # Generates uneven values like $4,532.87 or $12,041.13
            base = random.randint(amount_range[0] * 100, amount_range[1] * 100)
            cents = random.randint(1, 99)
            amount = float(base) + (cents / 100.0)
        else:
            # Clean thousands/hundreds values
            amount = float(random.randint(amount_range[0], amount_range[1]) * 100)
            
        if event == "investment":
            text = f"Event {i}: Owner invests ${amount:,.2f} cash into the business."
            entries = [
                {"account": "Cash", "type": "DEBIT", "amount": amount},
                {"account": "Owner's Equity", "type": "CREDIT", "amount": amount}
            ]
        elif event == "cash_sale":
            text = f"Event {i}: Performed services and received ${amount:,.2f} cash immediately."
            entries = [
                {"account": "Cash", "type": "DEBIT", "amount": amount},
                {"account": "Sales Revenue", "type": "CREDIT", "amount": amount}
            ]
        elif event == "credit_sale":
            text = f"Event {i}: Billed a customer ${amount:,.2f} for services completed on account."
            entries = [
                {"account": "Accounts Receivable", "type": "DEBIT", "amount": amount},
                {"account": "Sales Revenue", "type": "CREDIT", "amount": amount}
            ]
        elif event == "collection":
            text = f"Event {i}: Collected ${amount:,.2f} cash from a customer on an outstanding invoice."
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
            
    save_scenario(all_journal_entries)
    return prompts