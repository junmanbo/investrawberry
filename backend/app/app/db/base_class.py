from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr


# 모델 class 를 snake case 를 이용하여 테이블명 생성
def snake_case(s):
    result = ""
    for i, c in enumerate(s):
        if c.isupper() and i > 0:
            result += "_"
        result += c.lower()
    return result


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return snake_case(cls.__name__)
