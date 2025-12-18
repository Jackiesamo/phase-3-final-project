
import click
from datetime import datetime
from .db import init_db
from . import crud, utils

# ---------------- Helpers ----------------
def info(msg):
    click.echo(click.style(msg, fg="cyan"))

def success(msg):
    click.echo(click.style(msg, fg="green"))

def error(msg):
    click.echo(click.style(msg, fg="red"))

def format_timestamp(ts):
    if isinstance(ts, datetime):
        return ts.isoformat()
    elif isinstance(ts, str):
        return ts
    elif isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts).isoformat()
    return str(ts)

# ---------------- CLI Setup ----------------
@click.group()
def cli():
    """Budget Tracker CLI — manage users, accounts, and transactions."""
    pass

# ----- Setup -----
@cli.command("init-db")
def init_db_cmd():
    init_db()
    success("Database initialized.")

# ================= USER COMMANDS =================
@cli.group("user")
def user_group():
    pass

@user_group.command("add")
@click.argument("name")
@click.option("--email", default=None)
def user_add(name, email):
    try:
        u = crud.create_user(name, email)
        success(f"Created user [{u.id}] {u.name}")
    except Exception as e:
        error(str(e))

@user_group.command("list")
def user_list():
    users = crud.list_users()
    if not users:
        info("No users found.")
        return
    for u in users:
        info(f"[{u.id}] {u.name} — {u.email or 'no-email'}")

@user_group.command("update")
@click.argument("user_id", type=int)
@click.option("--name", default=None)
@click.option("--email", default=None)
def user_update(user_id, name, email):
    try:
        u = crud.update_user(user_id, name=name, email=email)
        success(f"Updated user [{u.id}] {u.name}")
    except Exception as e:
        error(str(e))

@user_group.command("delete")
@click.argument("user_id", type=int)
@click.confirmation_option(prompt="Delete user and all accounts?")
def user_delete(user_id):
    try:
        crud.delete_user(user_id)
        success("User deleted.")
    except Exception as e:
        error(str(e))

# ================= ACCOUNT COMMANDS =================
@cli.group("account")
def account_group():
    pass

@account_group.command("add")
@click.argument("user_id", type=int)
@click.argument("name")
@click.option("--balance", type=float, default=0.0)
def account_add(user_id, name, balance):
    try:
        a = crud.create_account(user_id, name, balance)
        success(f"Created account [{a.id}] {a.name} — {utils.format_currency(a.balance)}")
    except Exception as e:
        error(str(e))

@account_group.command("list")
@click.argument("user_id", type=int)
def account_list(user_id):
    accounts = crud.list_accounts_for_user(user_id)
    if not accounts:
        info("No accounts found.")
        return
    for a in accounts:
        info(f"[{a.id}] {a.name} — {utils.format_currency(a.balance)}")

@account_group.command("summary")
@click.argument("account_id", type=int)
def account_summary(account_id):
    try:
        info_data, txs = crud.account_summary(account_id)
        success(
            f"Account [{info_data['id']}] {info_data['name']} "
            f"Balance: {utils.format_currency(info_data['balance'])}"
        )
        for t in txs[:10]:
            info(
                f"[{t['id']}] {format_timestamp(t['timestamp'])} "
                f"{utils.format_currency(t['amount'])} "
                f"{t.get('description') or ''} ({t.get('category') or ''})"
            )
    except Exception as e:
        error(str(e))

@account_group.command("update")
@click.argument("account_id", type=int)
@click.option("--name", default=None)
def account_update(account_id, name):
    try:
        a = crud.update_account(account_id, name=name)
        success(f"Updated account [{a.id}] {a.name}")
    except Exception as e:
        error(str(e))

@account_group.command("delete")
@click.argument("account_id", type=int)
@click.confirmation_option(prompt="Delete account and all transactions?")
def account_delete(account_id):
    try:
        crud.delete_account(account_id)
        success("Account deleted.")
    except Exception as e:
        error(str(e))

# ================= TRANSACTION COMMANDS =================
@cli.group("tx")
def tx_group():
    pass

@tx_group.command("add")
@click.argument("account_id", type=int)
@click.argument("amount", type=float)
@click.option("--desc", default=None)
@click.option("--cat", default=None)
def tx_add(account_id, amount, desc, cat):
    try:
        tx = crud.add_transaction(account_id, amount, desc, cat)
        success(f"Added transaction [{tx.id}] {utils.format_currency(tx.amount)}")
    except Exception as e:
        error(str(e))

@tx_group.command("list")
@click.argument("account_id", type=int)
def tx_list(account_id):
    txs = crud.list_transactions_for_account(account_id)
    if not txs:
        info("No transactions.")
        return
    for t in txs:
        info(
            f"[{t.id}] {format_timestamp(t.timestamp)} "
            f"{utils.format_currency(t.amount)} "
            f"{t.description or ''} ({t.category or ''})"
        )

@tx_group.command("update")
@click.argument("tx_id", type=int)
@click.option("--amount", type=float, default=None)
@click.option("--desc", default=None)
@click.option("--cat", default=None)
def tx_update(tx_id, amount, desc, cat):
    try:
        tx = crud.update_transaction(tx_id, amount, desc, cat)
        success(f"Updated transaction [{tx.id}]")
    except Exception as e:
        error(str(e))

@tx_group.command("delete")
@click.argument("tx_id", type=int)
@click.confirmation_option(prompt="Delete this transaction?")
def tx_delete(tx_id):
    try:
        crud.delete_transaction(tx_id)
        success("Transaction deleted.")
    except Exception as e:
        error(str(e))

# ================= REPORTS =================
@cli.group("report")
def report_group():
    pass

@report_group.command("user-balance")
@click.argument("user_id", type=int)
def report_user_balance(user_id):
    total = crud.get_user_total_balance(user_id)
    success(f"User [{user_id}] total balance: {utils.format_currency(total)}")

@report_group.command("spending")
@click.argument("account_id", type=int)
def report_spending(account_id):
    txs = crud.list_transactions_for_account(account_id)
    tx_dicts = [
        {
            "amount": t.amount,
            "category": t.category or "Uncategorized",
            "timestamp": format_timestamp(t.timestamp),
        }
        for t in txs
    ]
    totals = utils.summarize_transactions(tx_dicts)
    if not totals:
        info("No transactions.")
        return
    success("Spending by category:")
    for cat, total in totals.items():
        info(f" - {cat}: {utils.format_currency(total)}")

# ---------------- Entry ----------------
if __name__ == "__main__":
    cli()
