from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator
from datetime import datetime

from api_framework.utils.model_validations import strint_to_bool, model_del_empty_str

from typing import TypedDict, NotRequired, Literal, Annotated, Any



JobContactTypes = Literal[
    "JOB","BILLING","Property Manager"
]

class JobContactParams(TypedDict):
    job_id: str
    first: NotRequired[str]
    last: NotRequired[str]
    phone: NotRequired[str]
    mobile: NotRequired[str]
    email: NotRequired[str]
    type: JobContactTypes

class JobContactResponse(BaseModel):
    model_config = ConfigDict(frozen = True)

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
        BeforeValidator(func=strint_to_bool)
    ]
    updated_at: Annotated[
        datetime|None,
        BeforeValidator(func=datetime.fromisoformat),
        Field(validation_alias="edit_date", default=None)
    ]
    first: str|None = None
    last: str|None = None
    phone: str|None = None
    mobile: str|None = None
    email: str|None = None
    type: JobContactTypes

    @model_validator(mode="before")
    @classmethod
    def del_empty_str(
        cls,
        data: dict[str, Any]
    ) -> dict[str, Any]:
        return model_del_empty_str(data)