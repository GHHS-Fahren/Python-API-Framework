from pydantic import BaseModel, ConfigDict, Field, AliasPath, ValidationError, model_validator
from datetime import datetime

from typing import Annotated, Any, Literal



class TransactionMetaResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    invoice_number: Annotated[
        str,
        Field(validation_alias="invoiceNumber")
    ]
    invoice_number_prefix: Annotated[
        str,
        Field(validation_alias="invoiceNumberPrefix")
    ]
    verify_minimum_value_to_pay: Annotated[
        bool,
        Field(validation_alias="verifyMinimumValueToPays")
    ]

class TransactionChargeSnapshotBankTransfer(BaseModel):
    model_config = ConfigDict(frozen=True)

    transaction_type: Literal["Bank Transfer"]
    mode: Literal["bank_transfer"]
    cheque_number: Annotated[
        str,
        Field(validation_alias=AliasPath(
            "cheque", "number"
        ))
    ]
    notes: str

class TransactionChargeSnapshotCardAutoPaymentMethods(BaseModel):
    model_config = ConfigDict(frozen=True)

    allow_redirects: str
    is_enabled: Annotated[
        bool,
        Field(validation_alias="enabled")
    ]

class TransactionChargeSnapshotCardChargeBillingAddress(BaseModel):
    model_config = ConfigDict(frozen=True)

    line1: str | None = None
    line2: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    post_code: Annotated[
        str | None,
        Field(validation_alias="postal_code")
    ] = None

class TransactionChargeSnapshotCardChargeBilling(BaseModel):
    model_config = ConfigDict(frozen=True)

    address: TransactionChargeSnapshotCardChargeBillingAddress
    email: str | None = None # Assumed type
    name: str | None = None # Assumed type
    phone: str | None = None # Assumed type
    tax_id: str | None = None # Assumed type

class TransactionChargeSnapshotCardMeta(BaseModel):
    model_config = ConfigDict(frozen=True)

    invoice_id: Annotated[
        str,
        Field(validation_alias="invoiceId")
    ]
    invoice_number: Annotated[
        str,
        Field(validation_alias="invoiceNumber")
    ]
    is_verify_min_val_to_pay: Annotated[
        bool,
        Field(validation_alias="verifyMinimumValueToPay")
    ]

class TransactionChargeSnapshotCardChargeOutcome(BaseModel):
    model_config = ConfigDict(frozen=True)

    # advice_code: ? | None = None
    # network_advice_code: ? | None = None
    # network_decline_code: ? | None = None
    network_status: str
    # reason: ? | None = None
    risk_level: str
    seller_message: str
    type: str

# class TransactionChargeSnapshotCardChargePaymentCardMethodDetails(BaseModel):
#     model_config = ConfigDict(frozen=True)

#     type: Literal["card"]
#     amount_authorized: float

#     @model_validator(mode="before")
#     @classmethod
#     def flatten_data(
#         cls,
#         data: dict[str,]
#     )

class TransactionChargeSnapshotCardCharge(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    amount: float
    amount_captured: float
    amount_refunded: float
    application: str
    application_fee: float | None = None # Assumed type
    application_fee_amount: float | None = None # Assumed type
    balance_transaction: str
    billing: TransactionChargeSnapshotCardChargeBilling | None = None
    calculated_statement_descriptor: str
    captured: bool
    created: float
    currency: str
    customer: str
    description: str
    # destination: ? | None = None
    # dispute: ? | None = None
    is_disputed: Annotated[
        bool,
        Field(validation_alias="disputed")
    ]
    # failure_balance_transaction: ? | None = None
    # failure_code: ? | None = None
    # failure_message: ? | None = None
    # fraud_details: dict[str, ?]
    invoice: str | None = None # Assumed type
    is_live: Annotated[
        bool,
        Field(validation_alias="livemode")
    ]
    meta: Annotated[
        TransactionChargeSnapshotCardMeta,
        Field(validation_alias="metadata")
    ]
    # on_behalf_of: ? | None = None
    # order: ? | None = None
    outcome: TransactionChargeSnapshotCardChargeOutcome
    is_paid: Annotated[
        bool,
        Field(validation_alias="paid")
    ]
    payment_intent: str
    payment_method: str
    # payment_method_details: TransactionChargeSnapshotCardChargePaymentCardMethodDetails
    # radar_options: dict[str, ?]
    receipt_email: str | None = None # Assumed type
    receipt_number: str | None = None # Assumed type
    receipt_url: str
    is_refunded: Annotated[
        bool,
        Field(validation_alias="refunded")
    ]
    # refunds: dict[str, str|list[?]|bool|float]
    # review: ? | None = None
    # shipping: ? | None = None
    # source: ? | None = None
    # source_transfer: ? | None = None
    # statement_descriptor: ? | None = None
    # statement_descriptor_suffix: ? | None = None
    status: str
    # transfer_data: ? | None = None
    # transfer_group: ? | None = None

class TransactionChargeSnapshotCardPaymentConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    parent: str

class TransactionChargeSnapshotCard(BaseModel):
    model_config = ConfigDict(frozen=True)

    transaction_type: Literal["Credit Card"]
    id: str
    object: str
    # allowed_payment_method_types: ? | None = None
    amount: float
    amount_capturable: float
    # amount_details: dict[str, dict[str, ?]]
    amount_received: float
    application: str
    application_fee_amount: float | None = None # Assumed type
    automatic_payment_methods: TransactionChargeSnapshotCardAutoPaymentMethods
    cancelled_at: datetime | None = None
    cancellation_reason: str | None = None # Assumed type
    capture_method: str
    charges: list[TransactionChargeSnapshotCardCharge]
    client_secret: str
    confirmation_method: str
    created: float
    currency: str
    customer: str
    # customer_account: ? | None = None
    description: str
    # excluded_payment_method_types: ? | None = None
    # invoice: ? | None = None
    # last_payment_error: ? | None = None
    latest_charge: str
    is_live: Annotated[
        bool,
        Field(validation_alias="livemode")
    ]
    # managed_payments: dict[str, bool|?]
    meta: Annotated[
        TransactionChargeSnapshotCardMeta,
        Field(validation_alias="metadata")
    ]
    # next_action: ? | None = None
    # on_behalf_of: ? | None = None
    payment_method_config: Annotated[
        TransactionChargeSnapshotCardPaymentConfig,
        Field(validation_alias="payment_method_configuration_details")
    ]
    # payment_method_options: dict[str, dict[str, str|None]]
    payment_method_types: tuple[str, ...]
    # processing: ? | None = None
    receipt_email: str | None = None # Assumed type
    # review: ? | None = None
    # setup_future_usage: ? | None = None
    # shared_payment_granted_token: ? | None = None
    # shipping: ? | None = None
    # source: ? | None = None
    # statement_descriptor: ? | None = None
    # statement_descriptor_suffix: ? | None = None
    status: str
    # transfer_data: ? | None = None
    # transfer_group: ? | None = None

    @model_validator(mode="before")
    @classmethod
    def listify_charges(
        cls,
        data: dict[str, Any]
    ) -> dict[str, Any]:
        new_data = {**data}
        charges = {**new_data["charges"]}
        if not charges["object"] == "list":
            raise ValidationError("Charges object is not a list!")
        if charges["has_more"] == True:
            raise ValidationError("Charges has more entries not listed!")
        new_data["charges"] = charges["data"]
        return new_data

class TransactionPaymentMethodCardResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    brand: str
    last4: str

class TransactionPaymentMethodResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    card: TransactionPaymentMethodCardResponse | None = None

class TransactionResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: Annotated[
        str,
        Field(validation_alias="_id")
    ]
    contact_id: Annotated[
        str | None,
        Field(validation_alias="contactId")
    ] =  None
    merged_from_contact_id: Annotated[
        str | None,
        Field(validation_alias="mergedFromContactId")
    ] =  None
    contact_name: Annotated[
        str | None,
        Field(validation_alias="contactName")
    ] =  None
    contact_email: Annotated[
        str | None,
        Field(validation_alias="contactEmail")
    ] =  None
    currency: str
    amount: float
    status: str
    is_live: Annotated[
        bool,
        Field(validation_alias="liveMode")
    ]
    entity_type: Annotated[
        str | None,
        Field(validation_alias="entityType")
    ] = None
    entity_id: Annotated[
        str | None,
        Field(validation_alias="entityId")
    ] = None
    entity_source_type: Annotated[
        str,
        Field(validation_alias="entitySourceType")
    ]
    entity_source_subtype: Annotated[
        str | None,
        Field(validation_alias="entitySourceSubType")
    ] = None
    entity_source_name: Annotated[
        str | None,
        Field(validation_alias="entitySourceName")
    ] = None
    entity_source_id: Annotated[
        str | None,
        Field(validation_alias="entitySourceId")
    ] = None
    entity_source_meta: TransactionMetaResponse | None = None
    subscription_id: Annotated[
        str | None,
        Field(validation_alias="subscriptionId")
    ] = None
    charge_id: Annotated[
        str | None,
        Field(validation_alias="chargeId")
    ] = None
    charge_snapshot: Annotated[
        TransactionChargeSnapshotBankTransfer | TransactionChargeSnapshotCard,
        Field(
            validation_alias="chargeSnapshot",
            discriminator="transaction_type"
        )
    ]
    payment_provider_type: Annotated[
        str | None,
        Field(validation_alias="paymentProviderType")
    ] = None
    payment_provider_connected_account: Annotated[
        str | None,
        Field(validation_alias="paymentProviderConnectedAccount")
    ] = None
    ip: Annotated[
        str | None,
        Field(validation_alias="ipAddress")
    ] = None
    created_at: Annotated[
        datetime,
        Field(validation_alias="createdAt")
    ]
    updated_at: Annotated[
        datetime,
        Field(validation_alias="updatedAt")
    ]
    amount_refunded: Annotated[
        float | None,
        Field(validation_alias="amountRefunded")
    ] = None
    payment_method: Annotated[
        TransactionPaymentMethodResponse,
        Field(validation_alias="paymentMethod")
    ]
    currency_code: Annotated[
        str,
        Field(validation_alias=AliasPath(
            "currencyOptions", "code"
        ))
    ]
    currency_symbol: Annotated[
        str,
        Field(validation_alias=AliasPath(
            "currencyOptions", "symbol"
        ))
    ]
    fulfilled_at: Annotated[
        datetime,
        Field(validation_alias="fulfilledAt")
    ]
    # paymentProviders: tuple[?, ...]
    # giftCardsMetadata: tuple[?, ...]
    created_by: Annotated[
        str | None,
        Field(validation_alias="createdBy")
    ] = None

    @model_validator(mode="before")
    @classmethod
    def determine_snapshot_type(
        cls,
        data: dict[str, Any]
    ) -> dict[str, Any]:
        new_data = {**data}
        charge_snapshot = {**new_data["chargeSnapshot"]}
        if charge_snapshot.get("mode") == "bank_transfer":
            charge_snapshot["transaction_type"] = "Bank Transfer"
        elif new_data["paymentMethod"].get("card") is not None:
            charge_snapshot["transaction_type"] = "Credit Card"
        else:
            raise ValidationError("Snapshot type is neither bank transfer nor cc!")
        new_data["chargeSnapshot"] = charge_snapshot
        return new_data