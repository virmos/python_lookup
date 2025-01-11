from pydantic import BaseModel, Field
from typing import Optional, Type, Any, Tuple
from copy import deepcopy

from pydantic import BaseModel, create_model, ConfigDict
from pydantic.fields import FieldInfo

def partial_model(model: Type[BaseModel]):
    def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new
    return create_model(
        f'Partial{model.__name__}',
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.__fields__.items()
        }
    )
@partial_model
class IPGroupModel(BaseModel):
    _id: str
    group_id: str
    description: str
    creator: str
    group_name: str
    priority: int
    visible: bool
    created_date: int
    last_update: int
    id_company: str
ip_group = IPGroupModel(id_company='1')
ip_group.id_company