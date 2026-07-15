from pydantic import BaseModel, ConfigDict, Field, BeforeValidator
from datetime import datetime

from typing import Annotated


class NoteResponse(BaseModel):
    model_config = ConfigDict(
        frozen = True
    )

    id: str = Field(
        validation_alias = "uuid"
    )
    is_active: Annotated[
        bool,
        BeforeValidator(bool)
    ] = Field(
        validation_alias = "active"
    )
    created_at: Annotated[
        datetime,
        BeforeValidator(datetime.fromisoformat)
    ] = Field(
        validation_alias = "create_date"
    )
    updated_at: Annotated[
        datetime,
        BeforeValidator(datetime.fromisoformat)
    ] = Field(
        validation_alias = "edit_date"
    )
    updated_by: str = Field(
        validation_alias = "edit_by_staff_uuid"
    )
    related_object: str
    related_object_id: str
    note: str
    is_action_required: Annotated[
        bool,
        BeforeValidator(lambda x: x == "1")
    ] = Field(
        validation_alias = "action_required"
    )
    action_completed_by: Annotated[
        str|None,
        BeforeValidator(lambda x: x if len(x)>0 else None)
    ] = Field(
        validation_alias = "action_completed_by_staff_uuid"
    )