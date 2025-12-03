import click
from .db import init_db
from . import crud, utils

# Helper for colored echoes
def info(msg):
    click.echo(click.style(msg, fg="cyan"))

def success(msg):
    click.echo(click.style(msg, fg="green"))

def error(msg):
    click.echo(click.style(msg, fg="red"))

@click.group()
def cli():
    """Budget Tracker CLI — manage users, accounts and transactions."""
    pass

# ----- Setup -----
@cli.command("init-db")
def init_db_cmd():
    """Create the database tables."""
    init_db()
    success("Database initialized (tables created).")

# ----- User commands -----
@cli.group("user")
def user_group():
    """User management commands."""
    pass

@user_group.command("add")
@click.argument("name")
@click.option("--email", default=None, help="Email address of the user")
def user_add(name, email):
    """Add a new user."""
    try:
        u = crud.create_user(name, email)
        success(f"Created user: [{u.id}] {u.name} ({u.email})")
    except Exception as e:
        error(f"Could not create user: {e}")

@user_group.command("list")
def user_list():
    """List all users."""
    users = crud.list_users()
    if not users:
        info("No users found.")
        return
    for u in users:
        info(f"[{u.id}] {u.name} — {u.email or 'no-email'}")

# ----- Account commands -----
@cli.group("account")
def account_group():
    """Account management commands."""
    pass

@account_group.command("add")
@click.argument("user_id", type=int)
@click.argument("name")
@click.option("--balance", type=float, default=0.0, help="Initial balance")
def account_add(user_id, name, balance):
    """Create an account for a user."""
    try:
        a = crud.create_account(user_id, name, balance)
        success(f"Account created: [{a.id}] {a.name} — balance {utils.format_currency(a.balance)}")
    except Exception as e:
        error(str(e))

@account_group.command("list")
@click.argument("user_id", type=int)
def account_list(user_id):
    """List accounts for a user."""
    accounts = crud.list_accounts_for_user(user_id)
    if not accounts:
        info("No accounts for this user.")
        return
    for a in accounts:
        info(f"[{a.id}] {a.name} — {utils.format_currency(a.balance)}")

@account_group.command("summary")
@click.argument("account_id", type=int)
def account_summary(account_id):
    """Show an account summary and latest transactions."""
    try:
        account_info, txs = crud.account_summary(account_id)
    except Exception as e:
        error(str(e))
        return
    success(f"Account: [{account_info['id']}] {account_info['name']} - Balance: {utils.format_currency(account_info['balance'])}")
    if not txs:
        info("No transactions yet.")
        return
    info("Recent transactions (most recent first):")
    for t in txs[:10]:
        ts = t.get("timestamp")
        desc = t.get("description") or ""
        cat = t.get("category") or ""
        click.echo(f" - [{t['id']}] {ts} {utils.format_currency(t['amount'])} {desc} ({cat})")

# ----- Transaction commands -----
@cli.group("tx")
def tx_group():
    """Transaction commands."""
    pass

@tx_group.command("add")
@click.argument("account_id", type=int)
@click.argument("amount", type=float)
@click.option("--desc", default=None, help="Description")
@click.option("--cat", default=None, help="Category")
def tx_add(account_id, amount, desc, cat):
    """Add a transaction. Positive amount increases balance; negative reduces."""
    try:
        tx = crud.add_transaction(account_id, amount, desc, cat)
        success(f"Transaction added: [{tx.id}] {utils.format_currency(tx.amount)}")
    except Exception as e:
        error(str(e))

@tx_group.command("list")
@click.argument("account_id", type=int)
def tx_list(account_id):
    """List transactions for an account."""
    txs = crud.list_transactions_for_account(account_id)
    if not txs:
        info("No transactions.")
        return
    for t in txs:
        info(f"[{t.id}] {t.timestamp.isoformat()} {utils.format_currency(t.amount)} — {t.description or ''} ({t.category or ''})")

@tx_group.command("export")
@click.argument("account_id", type=int)
@click.option("--out", default=None, help="Path to save CSV (if omitted prints CSV to stdout)")
def tx_export(account_id, out):
    """Export transactions CSV for an account."""
    txs = crud.list_transactions_for_account(account_id)
    tx_dicts = [
        {
            "id": t.id,
            "account_id": t.account_id,
            "amount": t.amount,
            "timestamp": t.timestamp.isoformat(),
            "description": t.description,
            "category": t.category,
        } for t in txs
    ]
    csv_data = utils.transactions_to_csv(tx_dicts)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(csv_data)
        success(f"Wrote CSV to {out}")
    else:
        click.echo(csv_data)

# ----- Reports -----
@cli.group("report")
def report_group():
    """Reporting commands."""
    pass

@report_group.command("user-balance")
@click.argument("user_id", type=int)
def report_user_balance(user_id):
    """Show total balance across all accounts for a user."""
    total = crud.get_user_total_balance(user_id)
    success(f"User [{user_id}] total balance: {utils.format_currency(total)}")

@report_group.command("spending")
@click.argument("account_id", type=int)
def report_spending(account_id):
    """Show spending totals by category for an account."""
    txs = crud.list_transactions_for_account(account_id)
    tx_dicts = [
        {"id": t.id, "amount": t.amount, "category": t.category or "Uncategorized", "timestamp": t.timestamp.isoformat()}
        for t in txs
    ]
    totals = utils.summarize_transactions(tx_dicts)
    if not totals:
        info("No transactions to summarize.")
        return
    success("Spending by category:")
    for cat, total in totals.items():
        info(f" - {cat}: {utils.format_currency(total)}")

# ----- CLI entrypoint -----
if __name__ == "__main__":
    cli()
