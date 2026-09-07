from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from datetime import datetime

from typing import Annotated, Literal



class CamelResponseModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        alias_generator=to_camel
    )


class PriceMembershipOffersResponse(CamelResponseModel):
    id: Annotated[
        str,
        Field(validation_alias="_id")
    ]
    label: str
    value: str

class PriceRecurringResponse(CamelResponseModel):
    interval: Literal["day", "month", "week", "year"]
    count: Annotated[
        float,
        Field(validation_alias="intervalCount")
    ]

class PriceResponse(CamelResponseModel):
    id: Annotated[
        str,
        Field(validation_alias="_id")
    ]
    variant_option_ids: tuple[str, ...] | None = None
    product: str
    user_id: str | None = None
    name: str
    type: Literal["one_time", "recurring"]
    currency: str
    amount: float
    recurring: PriceRecurringResponse | None = None
    created_at: datetime
    updated_at: datetime
    compare_at_price: float | None = None
    is_track_inventory: Annotated[
        bool,
        Field(validation_alias="trackInventory")
    ]
    available_quantity: float | None = None
    is_out_of_stock_purchase_allowed: Annotated[
        bool | None,
        Field(validation_alias="allowOutOfStockPurchases")
    ] = None