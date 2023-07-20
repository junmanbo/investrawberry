from typing import Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.simple_transaction import SimpleTransaction
from app.schemas.simple_transaction import SimpleTransactionCreate, SimpleTransactionUpdate


class CRUDSimpleTransaction(CRUDBase[SimpleTransaction, SimpleTransactionCreate, SimpleTransactionUpdate]):
    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[SimpleTransaction]:
        return db.query(SimpleTransaction).filter(SimpleTransaction.uuid == uuid).first()


simple_transaction = CRUDSimpleTransaction(SimpleTransaction)

