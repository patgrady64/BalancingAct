# BalancingAct - QuickBooks Practice Engine

**BalancingAct** is a lightweight, local desktop application designed to act as a simulator and training ground for mastering double-entry bookkeeping and accounting principles.

Instead of searching for random static math problems online, BalancingAct generates dynamic, randomized business periods with varying levels of difficulty. You use these generated plain-English prompts to practice entering debits and credits in your live accounting sandbox (like QuickBooks), track your final account balances, and use the built-in validation modal to grade your score instantly.

---

## 🚀 Key Features

- **Dynamic Scenario Generation:** Instantly creates localized pools of random transaction streams (_Cash, Accounts Receivable, Owner's Equity, and Sales Revenue_).
- **Four Difficulty Tiers:** Scales with your skillset:
  - **Easy:** 3–4 basic transactions with clean, round values.
  - **Medium:** 6–8 transactions with slightly larger intervals.
  - **Hard:** 10–12 transactions introducing messy, un-even real-world decimal structures.
  - **Hardest:** 15–20 high-volume, rapid-fire transactions to push tracking accuracy under load.
- **The "Check Answer" Modal:** A submission form that securely tests your calculated values against the application's engine, returning a breakdown of mismatches and correct solutions.
- **Flawless Dark Mode Theme:** Designed with a high-contrast dark aesthetic that integrates cleanly with modern developer environments.
- **Self-Contained Architecture:** Uses a localized file-system database requiring no external network API calls.

---

## 🛠️ Tech Stack & Architecture

- **Language:** Python 3.x
- **GUI Framework:** PySide6 (The official Qt for Python bindings)
- **Database Layer:** SQLite3 (Core relational engine, self-contained inside `balancing_act.db`)

### Codebase Organization

```text
balancing_act/
│
├── main.py              # Entry point. Handles PySide6 application layout and Dialog Modals.
├── generator.py         # Generation Engine. Creates random periods based on difficulty constraints.
├── database.py          # Data abstraction layer. Sets up SQLite schema and aggregates answer keys.
├── requirements.txt     # Generated dependency tracking manifest.
└── .gitignore           # Keeps venv, cached files, and local binaries out of Git tracking.
```
