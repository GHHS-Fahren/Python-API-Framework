from pydantic import BaseModel, Field, field_validator



class EmbeddedContactResponse(BaseModel):
    id: str
    name: str
    company_name: str = Field(
        serialization_alias = "companyName"
    )
    email: str
    phone: str
    tags: tuple[str, ...]

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(
        cls,
        tags: list[str, ...]
    ) -> tuple[str, ...]:
        return tuple(tags)