from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from datetime import datetime

from typing import Annotated, Literal



class CamelResponseModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        alias_generator=to_camel
    )


class ProductMediasResponse(CamelResponseModel):
    id: str
    title: str | None = None
    url: str
    type: Literal["image", "video"]
    is_featured: bool | None = None
    price_ids: tuple[str, ...] | None = None

class ProductVariantsResponse(CamelResponseModel):
    id: str
    name: str
    # options

class ProductLabelResponse(CamelResponseModel):
    title: str
    start_at: Annotated[
        datetime | None,
        Field(validation_alias="startDate")
    ] = None
    end_at: Annotated[
        datetime | None,
        Field(validation_alias="endDate")
    ] = None

class ProductResponse(CamelResponseModel):
    id: Annotated[
        str,
        Field(validation_alias="_id")
    ]
    created_at: datetime
    updated_at: datetime
    name: str
    description: str | None = None
    product_type: Literal[
        "DIGITAL", "PHYSICAL", "SERVICE", "PHYSICAL/DIGITAL"
    ]
    image: str | None = None
    statement_descriptor: str | None = None
    is_available_in_store: Annotated[
        bool | None,
        Field(validation_alias="availableInStore")
    ] = None
    medias: tuple[ProductMediasResponse, ...] | None = None
    variants: tuple[ProductVariantsResponse, ...] | None = None
    categories: Annotated[
        tuple[str, ...] | None,
        Field(validation_alias="collectionIds")
    ] = None
    is_taxes_enabled: bool
    taxes: tuple[str, ...]
    automatic_tax_category_id: str | None = None
    is_label_enabled: bool = False
    label: ProductLabelResponse | None = None
    slug: str | None = None
    # seo: {title: str, description: str}
    is_tax_inclusive: Annotated[
        bool | None,
        Field(validation_alias="taxInclusive")
    ] = None
    prices: tuple[str, ...] | None = None
    # There are undocumented fields ._.