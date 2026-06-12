from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime, date

from api_framework.models.common.ghl_contact \
    import EmbeddedContactResponse
from api_framework.utils.deep_freeze import deep_freeze

from typing import Mapping, Any, Optional, Literal



class OpportunityParams(TypedDict):
    opportunity_id: str|None
    pipeline_id: str|None
    pipeline_stage_id: str|None
    followers: list[str]|None
    is_remove_all_followers: bool|None
    followers_action_type: str|None
    name: str|None
    status: Literal["open", "won", "lost", "abandoned", "all"]|None
    value: float|None
    forecast_expected_close_date: datetime|None
    forecast_probability: float|None
    assigned_to: str|None
    lost_reason_id: str|None

class OpportunityResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    value: Optional[float] = Field(
        default=None,
        serialization_alias="monetaryValue"
    )
    pipeline_id: str = Field(
        serialization_alias="pipelineId"
    )
    pipeline_stage_id: str = Field(
        serialization_alias="pipelineStageId"
    )
    assigned_to: Optional[str] = Field(
        default=None,
        serialization_alias="assignedTo"
    )
    status: str
    source: Optional[str] = None
    last_status_change_at: Optional[datetime] = Field(
        default=None,
        serialization_alias="lastStatusChangeAt"
    )
    last_stage_change_at: Optional[datetime] = Field(
        default=None,
        serialization_alias="lastStageChangeAt"
    )
    last_action_date: Optional[datetime] = Field(
        default=None,
        serialization_alias="lastActionDate"
    )
    index_version: Optional[str] = Field(
        default=None,
        serialization_alias="indexVersion"
    )
    created_at: datetime = Field(
        serialization_alias="createdAt"
    )
    updated_at: datetime = Field(
        serialization_alias="updatedAt"
    )
    forecast_expected_close_date: Optional[date] = Field(
        default=None,
        serialization_alias="forecastExpectedCloseDate"
    )
    forecast_original_close_date: Optional[date] = Field(
        default=None,
        serialization_alias="forecastOriginalCloseDate"
    )
    forecast_slippage_count: Optional[int] = Field(
        default=None,
        serialization_alias="forecastSlippageCount"
    )
    forecast_days_slipped: Optional[int] = Field(
        default=None,
        serialization_alias="forecastDaysSlipped"
    )
    forecast_last_slipped_at: Optional[datetime] = Field(
        default=None,
        serialization_alias="forecastLastSlippedAt"
    )
    forecast_probability: Optional[float] = Field(
        default=None,
        serialization_alias="forecastProbability"
    )
    effective_probability: Optional[float] = Field(
        default=None,
        serialization_alias="effectiveProbability"
    )
    contact_id: Optional[str] = Field(
        default=None,
        serialization_alias="contactId"
    )
    location_id: str = Field(
        serialization_alias="locationId"
    )
    contact: Optional[EmbeddedContactResponse] = None
    notes: tuple[Any, ...] = Field(default_factory=tuple)
    tasks: tuple[Any, ...] = Field(default_factory=tuple)
    calendar_events: tuple[Any, ...] = Field(
        default_factory=tuple,
        serialization_alias="calendarEvents"
    )
    lost_reason_id: Optional[str] = Field(
        default=None,
        serialization_alias="lostReasonId"
    )
    custom_fields: tuple[Mapping[str, Any], ...] = Field(
        default_factory=tuple,
        serialization_alias="customFields"
    )
    followers: tuple[str, ...] = Field(default_factory=tuple)
    external_object_id: Optional[str] = Field(
        default=None,
        serialization_alias="externalObjectId"
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
        value: Optional[str]
    ) -> Optional[date]:
        return date.fromisoformat(value)

    @field_validator(
        "notes", "tasks", "calendar_events",
        "custom_fields", "followers",
        mode="before"
    )
    @classmethod
    def validate_freezable(
        cls,
        value: Any
    ) -> Any:
        """
        Deep-freezes mapping fields to preserve model immutability.
        """
        return deep_freeze(value)