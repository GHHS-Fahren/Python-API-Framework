from pydantic import BaseModel, Field, model_validator



class AssociationResponse(BaseModel):
    class _CustomObjectData(BaseModel):
        label: str
        key: str

    id: str
    key: str = Field(
        validation_alias = "key"
    )
    type: str = Field(
        validation_alias = "associationType"
    )
    first_object: _CustomObjectData
    second_object: _CustomObjectData

    @classmethod
    @model_validator(mode="before")
    def validate_objects(
        cls,
        data: dict[str, str]
    ) -> dict[str, str]:
        data["first_object"] = {
            "label": data.pop("firstObjectLabel"),
            "key": data.pop("firstObjectKey")
        }
        data["second_object"] = {
            "label": data.pop("secondObjectLabel"),
            "key": data.pop("secondObjectKey")
        }
        return data