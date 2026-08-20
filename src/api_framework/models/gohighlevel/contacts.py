from pydantic import BaseModel, ConfigDict, Field, BeforeValidator
from datetime import datetime

from typing import Annotated



class ContactNoteResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    body: str
    user_id: Annotated[
        str,
        Field(validation_alias="userId")
    ]
    created_at: Annotated[
        datetime,
        Field(validation_alias="dateAdded"),
        BeforeValidator(func=datetime.fromisoformat)
    ]
    contact_id: Annotated[
        str,
        Field(validation_alias="contactId")
    ]
    title: str|None = None
    colour: str|None = None
    is_pinned: Annotated[
        bool,
        Field(validation_alias="pinned")
    ]