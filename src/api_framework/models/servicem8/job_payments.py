from pydantic import AfterValidator, BaseModel, ConfigDict, Field, BeforeValidator
from datetime import datetime
from decimal import Decimal

from api_framework.utils.model_validations import strint_to_bool, str_to_strnone

from typing import Annotated, TypedDict, NotRequired



class JobPaymentParams(TypedDict):
    job_id: str
    paid_at: NotRequired[datetime]
    actioned_by: NotRequired[str]
    amount: Decimal
    method: NotRequired[str]
    note: NotRequired[str]
    attachment_id: NotRequired[str]

class JobPaymentResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: Annotated[
        str,
        Field(validation_alias="uuid")
    ]
    job_id: Annotated[
        str,
        Field(validation_alias="job_uuid")
    ]
    is_active: Annotated[
        bool,
        Field(validation_alias="active"),
    ]
    paid_at: Annotated[
        datetime,
        Field(validation_alias="timestamp")
    ]
    updated_at: Annotated[
        datetime,
        Field(validation_alias="edit_date")
    ]
    actioned_by: Annotated[
        str | None,
        Field(validation_alias="actioned_by_uuid"),
        AfterValidator(str_to_strnone)
    ] = None
    amount: Decimal
    method: Annotated[
        str | None,
        AfterValidator(str_to_strnone)
    ] = None
    note: Annotated[
        str | None,
        AfterValidator(str_to_strnone)
    ] = None
    attachment_id: Annotated[
        str | None,
        Field(validation_alias="attachment_uuid"),
        AfterValidator(str_to_strnone)
    ] = None
    is_deposit: Annotated[
        bool,
        BeforeValidator(strint_to_bool)
    ]