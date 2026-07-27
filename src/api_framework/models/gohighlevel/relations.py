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
        data: dict[str, str|dict[str,str]]
    ) -> dict[str, str|dict[str,str]]:
        """
        Converts the first and second object data to a structure that
        pydantic can parse to the sub classes
        """
        new_data = {**data}
        new_data["first_object"] = {
            "id": new_data.pop("firstRecordId"),
            "key": new_data.pop("firstObjectKey")
        }
        new_data["second_object"] = {
            "id": new_data.pop("secondRecordId"),
            "key": new_data.pop("secondObjectKey")
        }
        return new_data