from typing import Optional, List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Transaction]:
        return db.query(Transaction).filter(Transaction.uuid == uuid).first()

    def get_open_transactions(self, db: Session, *, user_id: int) -> List[Transaction]:
        return (
            db.query(self.model)
            .filter(Transaction.status == "open", Transaction.user_id == user_id)
            .all()
        )


transaction = CRUDTransaction(Transaction)
