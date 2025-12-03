# from sqlalchemy import select, func, update
# from sqlalchemy.exc import NoResultFound
# from .db import SessionLocal
# from .models import User, Account, Transaction
# from typing import List, Dict, Tuple

# # ---------- User CRUD ----------
# def create_user(name: str, email: str | None = None) -> User:
#     with SessionLocal() as session:
#         user = User(name=name, email=email)
#         session.add(user)
#         session.commit()
#         session.refresh(user)
#         return user

# def get_user(user_id: int) -> User | None:
#     with SessionLocal() as session:
#         return session.get(User, user_id)

# def list_users() -> List[User]:
#     with SessionLocal() as session:
#         stmt = select(User).order_by(User.id)
#         return session.scalars(stmt).all()

# # ---------- Account CRUD ----------
# def create_account(user_id: int, name: str, initial_balance: float = 0.0) -> Account:
#     with SessionLocal() as session:
#         # verify user exists
#         user = session.get(User, user_id)
#         if not user:
#             raise ValueError(f"User with id {user_id} not found")
#         account = Account(name=name, user_id=user_id, balance=float(initial_balance))
#         session.add(account)
#         session.commit()
#         session.refresh(account)
#         return account

# def get_account(account_id: int) -> Account | None:
#     with SessionLocal() as session:
#         return session.get(Account, account_id)

# def list_accounts_for_user(user_id: int) -> List[Account]:
#     with SessionLocal() as session:
#         stmt = select(Account).where(Account.user_id == user_id).order_by(Account.id)
#         return session.scalars(stmt).all()

# # ---------- Transactions ----------
# def add_transaction(account_id: int, amount: float, description: str | None = None, category: str | None = None) -> Transaction:
#     """
#     Add a transaction and update the account balance atomically within the same session.
#     Positive amount increases balance, negative decreases.
#     """
#     with SessionLocal() as session:
#         account = session.get(Account, account_id)
#         if not account:
#             raise ValueError(f"Account {account_id} not found")
#         tx = Transaction(account_id=account_id, amount=float(amount), description=description, category=category)
#         # adjust balance
#         account.balance = (account.balance or 0.0) + float(amount)
#         session.add(tx)
#         session.add(account)
#         session.commit()
#         session.refresh(tx)
#         return tx

# def list_transactions_for_account(account_id: int) -> List[Transaction]:
#     with SessionLocal() as session:
#         stmt = select(Transaction).where(Transaction.account_id == account_id).order_by(Transaction.timestamp.desc())
#         return session.scalars(stmt).all()

# def account_summary(account_id: int) -> Tuple[Dict, List[Dict]]:
#     with SessionLocal() as session:
#         account = session.get(Account, account_id)
#         if not account:
#             raise ValueError(f"Account {account_id} not found")
#         txs = [
#             {
#                 "id": t.id,
#                 "account_id": t.account_id,
#                 "amount": t.amount,
#                 "timestamp": t.timestamp.isoformat(),
#                 "description": t.description,
#                 "category": t.category,
#             } for t in sorted(account.transactions, key=lambda tt: tt.timestamp, reverse=True)
#         ]
#         account_info = {"id": account.id, "name": account.name, "balance": float(account.balance), "user_id": account.user_id}
#         return account_info, txs

# # ---------- Aggregates ----------
# def get_user_total_balance(user_id: int) -> float:
#     with SessionLocal() as session:
#         stmt = select(func.sum(Account.balance)).where(Account.user_id == user_id)
#         total = session.scalar(stmt)
#         return float(total or 0.0)
