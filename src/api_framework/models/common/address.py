from pydantic import BaseModel, ConfigDict



class Address(BaseModel):
    latitude: float|None = None
    longitude: float|None = None
    number: str|None = None
    street: str|None = None
    city: str|None = None
    state: str|None = None
    postcode: str|None = None
    country: str|None = None
    full_address: str|None = None

class FrozenAddress(Address):
    model_config = ConfigDict(frozen=True)