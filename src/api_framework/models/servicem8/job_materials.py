from pydantic import BaseModel, BeforeValidator, ConfigDict, Field
from datetime import datetime

from api_framework.utils.model_validations import strint_to_bool

from typing import Annotated, TypedDict



class JobMaterialParams(TypedDict):
    job_id: str
    material_id: str
    quantity: float
    material_bundle_id: str|None
    sort_order: int|None
    name: str|None
    cost: float|None
    price: float|None
    tax_rate_id: str|None
    displayed_cost: float|None
    displayed_amount: float|None
    is_displayed_tax_inclusive: bool|None

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
    tax_rate_id: str
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
    ]

