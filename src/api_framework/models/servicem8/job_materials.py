from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, \
    model_validator
from datetime import datetime

from api_framework.utils.model_validations \
    import strint_to_bool, model_del_empty_str

from typing import Annotated, TypedDict, NotRequired, Any



class JobMaterialParams(TypedDict):
    job_id: NotRequired[str]
    material_id: str
    quantity: float
    material_bundle_id: NotRequired[str]
    sort_order: NotRequired[int]
    name: NotRequired[str]
    cost: NotRequired[float]
    price: NotRequired[float]
    tax_rate_id: NotRequired[str]
    displayed_cost: NotRequired[float]
    displayed_amount: NotRequired[float]
    is_displayed_tax_inclusive: NotRequired[bool]

class JobMaterialResponse(BaseModel):
    model_config = ConfigDict(frozen = True)

    id: str = Field(
        validation_alias = "uuid"
    )
    job_id: str = Field(
        validation_alias = "job_uuid"
    )
    material_id: str = Field(
        validation_alias = "material_uuid"
    )
    material_bundle_id: str|None = Field(
        validation_alias = "job_material_bundle_uuid",
        default = None
    )
    is_active: Annotated[
        bool,
        BeforeValidator(strint_to_bool)
    ] = Field(
        validation_alias = "active"
    )
    updated_at: Annotated[
        datetime|None,
        BeforeValidator(datetime.fromisoformat)
    ] = Field(
        validation_alias = "edit_date",
        default = None
    )
    sort_order: Annotated[
        int,
        BeforeValidator(int)
    ]
    name: str|None = None
    quantity: Annotated[
        float,
        BeforeValidator(float)
    ]
    cost: Annotated[
        float,
        BeforeValidator(float)
    ]
    price: Annotated[
        float,
        BeforeValidator(float)
    ]
    tax_rate_id: str = Field(
        validation_alias = "tax_rate_uuid"
    )
    displayed_cost: Annotated[
        float,
        BeforeValidator(float)
    ]
    displayed_amount: Annotated[
        float,
        BeforeValidator(float)
    ]
    is_displayed_tax_inclusive: Annotated[
        bool,
        BeforeValidator(strint_to_bool)
    ] = Field(
        validation_alias = "displayed_amount_is_tax_inclusive"
    )

    @model_validator(mode="before")
    @classmethod
    def del_empty_str(
        cls,
        data: dict[str, Any]
    ) -> dict[str, Any]:
        return model_del_empty_str(data)