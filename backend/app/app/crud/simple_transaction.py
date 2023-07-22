from typing import Optional, List
from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.simple_transaction import SimpleTransaction
from app.schemas.simple_transaction import SimpleTransactionCreate, SimpleTransactionUpdate


class CRUDSimpleTransaction(CRUDBase[SimpleTransaction, SimpleTransactionCreate, SimpleTransactionUpdate]):
    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[SimpleTransaction]:
        return db.query(SimpleTransaction).filter(SimpleTransaction.uuid == uuid).first()

    def get_open_transactions(
        self, db: Session, *, user_id: int
    ) -> List[SimpleTransaction]:
        return db.query(self.model).options(joinedload(SimpleTransaction.ticker)).filter(SimpleTransaction.status == "open",
                                                                                         SimpleTransaction.user_id == user_id).all()


simple_transaction = CRUDSimpleTransaction(SimpleTransaction)

