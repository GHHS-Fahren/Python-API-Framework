from pytest import fixture, raises, skip
from typing import Any
from pydantic import BaseModel, ValidationError



class BaseFrozenModelTests:
    model_class: type[BaseModel] = None
    api_payload: dict[str, Any] = {}
    required_field: tuple[str, str]|None = None
    optional_field: tuple[str, str]|None = None
    aliased_field: tuple[str, str]|None = None

    @fixture(autouse = True)
    def setup(self) -> None:
        raise NotImplementedError("Subclasses must impliment setup")

    def build(self, model_data: dict[str, Any]) -> BaseModel:
        return self.model_class.model_validate(model_data)
    
    def del_field(self, field: str) -> dict[str, Any]:
        model_data = {**self.api_payload}
        del model_data[field]
        return model_data
    
    def test_for_valid_parse(self):
        if self.aliased_field is None:
            skip("Aliased Field not defined")
        alias, field = self.aliased_field
        instance = self.build(self.api_payload)
        assert getattr(instance, field) == self.api_payload[alias]
    
    def test_for_optional_fields(self):
        if self.optional_field is None:
            skip("Optional Field not defined")
        alias, field = self.optional_field
        model_data = {**self.api_payload}
        if alias: del model_data[alias]
        instance = self.build(model_data)
        assert getattr(instance, field) is None
    
    def test_for_raise_on_required_missing(self):
        if self.required_field is None:
            skip("Required Field not defined")
        alias, _ = self.required_field
        model_data = {**self.api_payload}
        del model_data[alias]
        with raises(ValidationError):
            _ = self.build(model_data)
    
    def test_for_model_immutibility(self):
        if self.required_field is None:
            skip("Required Field not defined")
        _, field = self.required_field
        instance = self.build(self.api_payload)
        with raises(ValidationError):
            setattr(instance, field, "mutated")
    
    def test_for_model_hashibility(self):
        instance = self.build(self.api_payload)
        assert hash(instance) is not None
        assert instance in {instance} # pyright: ignore[reportUnhashable]
    
    def test_for_model_equality(self):
        instance_a=self.build(self.api_payload)
        instance_b=self.build(self.api_payload)
        assert instance_a == instance_b
        assert hash(instance_a) == hash(instance_b)