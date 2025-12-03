from typing import Iterable, List, Dict
from datetime import datetime
import csv
from io import StringIO

def format_currency(amount: float) -> str:
    """
    Format amount into a simple currency string (KES).
    Adjust the prefix to your preferred currency if needed.
    """
    return f"KES {amount:,.2f}"

def summarize_transactions(txs: Iterable[Dict]) -> Dict[str, float]:
    """
    Given an iterable of transaction dicts containing 'category' and 'amount',
    returns a mapping category -> total_amount.
    """
    totals: Dict[str, float] = {}
    for t in txs:
        cat = t.get("category") or "Uncategorized"
        totals[cat] = totals.get(cat, 0.0) + float(t.get("amount", 0.0))
    return totals

def transactions_to_csv(txs: Iterable[Dict]) -> str:
    """
    Convert transactions (list of dict) to CSV string and return it.
    Columns: id,account_id,amount,timestamp,description,category
    """
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id","account_id","amount","timestamp","description","category"])
    for t in txs:
        writer.writerow([
            t.get("id"),
            t.get("account_id"),
            t.get("amount"),
            t.get("timestamp"),
            t.get("description"),
            t.get("category"),
        ])
    return output.getvalue()
