import re
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import mapped_column, DeclarativeBase, declared_attr


class Base(AsyncAttrs, DeclarativeBase):

    @declared_attr.directive
    def __tablename__(cls) -> str:
        snake_case_name = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        return f"{snake_case_name}"
    
int_pk = Annotated[int, mapped_column(primary_key=True)]