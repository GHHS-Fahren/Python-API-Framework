from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime

from typing import Any, Literal, TypedDict, NotRequired



class OpportunityParams(TypedDict):
    opportunity_id: NotRequired[str]
    pipeline_id: NotRequired[str]
    contact_id: str
    pipeline_stage_id: NotRequired[str]
    followers: NotRequired[list[str]]
    is_remove_all_followers: NotRequired[bool]
    followers_action_type: NotRequired[str]
    name: NotRequired[str]
    status: NotRequired[Literal["open", "won", "lost", "abandoned", "all"]]
    value: NotRequired[float]
    forecast_expected_close_date: NotRequired[datetime]
    forecast_probability: NotRequired[float]
    assigned_to: NotRequired[str]
    lost_reason_id: NotRequired[str]
    custom_fields: NotRequired[list[dict[str, Any]]]

class OpportunityContactResponse(BaseModel):
    model_config = ConfigDict(frozen = True)

    id: str
    name: str
    email: str
    phone: str|None = None
    tags: tuple[str, ...]
    followers: tuple[str, ...]

    @field_validator("tags", "followers", mode="before")
    @classmethod
    def validate_tags(
        cls,
        tags: list[str]
    ) -> tuple[str, ...]:
        return tuple(tags)

class OpportunityResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    value: float|None = Field(
        default=None,
        validation_alias="monetaryValue"
    )
    pipeline_id: str = Field(
        validation_alias="pipelineId"
    )
    pipeline_stage_id: str = Field(
        validation_alias="pipelineStageId"
    )
    assigned_to: str|None = Field(
        default=None,
        validation_alias="assignedTo"
    )
    status: str
    source: str|None = None
    last_status_change_at: datetime|None = Field(
        default=None,
        validation_alias="lastStatusChangeAt"
    )
    last_stage_change_at: datetime|None = Field(
        default=None,
        validation_alias="lastStageChangeAt"
    )
    last_action_date: datetime|None = Field(
        default=None,
        validation_alias="lastActionDate"
    )
    index_version: int|None = Field(
        default=None,
        validation_alias="indexVersion"
    )
    created_at: datetime = Field(
        validation_alias="createdAt"
    )
    updated_at: datetime = Field(
        validation_alias="updatedAt"
    )
    forecast_expected_close_date: datetime|None = Field(
        default=None,
        validation_alias="forecastExpectedCloseDate"
    )
    forecast_original_close_date: datetime|None = Field(
        default=None,
        validation_alias="forecastOriginalCloseDate"
    )
    forecast_slippage_count: int|None = Field(
        default=None,
        validation_alias="forecastSlippageCount"
    )
    forecast_days_slipped: int|None = Field(
        default=None,
        validation_alias="forecastDaysSlipped"
    )
    forecast_last_slipped_at: datetime|None = Field(
        default=None,
        validation_alias="forecastLastSlippedAt"
    )
    forecast_probability: float|None = Field(
        default=None,
        validation_alias="forecastProbability"
    )
    effective_probability: float|None = Field(
        default=None,
        validation_alias="effectiveProbability"
    )
    contact_id: str = Field(
        validation_alias="contactId"
    )
    location_id: str = Field(
        validation_alias="locationId"
    )
    contact: OpportunityContactResponse|None = None
    notes: tuple[Any, ...] = Field(default_factory=tuple)
    tasks: tuple[Any, ...] = Field(default_factory=tuple)
    calendar_events: tuple[Any, ...] = Field(
        default_factory=tuple,
        validation_alias="calendarEvents"
    )
    lost_reason_id: str|None = Field(
        default=None,
        validation_alias="lostReasonId"
    )
    custom_fields: tuple[dict[str, Any], ...] = Field(
        default_factory=tuple,
        validation_alias="customFields"
    )
    followers: tuple[str, ...] = Field(default_factory=tuple)
    external_object_id: str|None = Field(
        default=None,
        validation_alias="externalObjectId"
    )

    @field_validator(
        "created_at", "updated_at",
        "last_status_change_at", "last_stage_change_at",
        "last_action_date", "forecast_last_slipped_at",
        "forecast_expected_close_date",
        "forecast_original_close_date",
        mode="before"
    )
    @classmethod
    def validate_dates(
        cls,
        value: str
    ) -> datetime:
        return datetime.fromisoformat(value)

    # @field_validator(
    #     "notes", "tasks", "calendar_events",
    #     "followers",
    #     mode="before"
    # )
    # @classmethod
    # def validate_freezable(
    #     cls,
    #     value: Any
    # ) -> Any:
    #     """
    #     Deep-freezes mapping fields to preserve model immutability.
    #     """
    #     return deep_freeze(value)