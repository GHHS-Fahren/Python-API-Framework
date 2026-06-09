from pydantic import BaseModel, ConfigDict, Field, model_validator



class RelationResponse(BaseModel):
    class _CustomObjectData(BaseModel):
        model_config = ConfigDict(frozen=True)
        id: str
        key: str

    model_config = ConfigDict(
        frozen = True
    )
    
    id: str
    association_id: str = Field(
        validation_alias = "associationId"
    )
    first_object: _CustomObjectData
    second_object: _CustomObjectData

    @model_validator(mode="before")
    @classmethod
    def validate_objects(
        cls,
        data: dict[str, str]
    ) -> dict[str, str]:
        """
        Converts the first and second object data to a structure that
        pydantic can parse to the sub classes
        """
        data["first_object"] = {
            "id": data.pop("firstRecordId"),
            "key": data.pop("firstObjectKey")
        }
        data["second_object"] = {
            "id": data.pop("secondRecordId"),
            "key": data.pop("secondObjectKey")
        }
        return data