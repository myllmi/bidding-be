from datetime import datetime

from schemas.camel_schema import CamelModelBase


class CustomerModelRes(CamelModelBase):
    id: str | None
    customer_name: str
    vat_number: str | None
    phone_number: str | None
    contact_name: str | None
    address: str | None
    city: str | None
    district: str | None
    country: str | None
    confirmed_at: datetime | None
    created_at: datetime
    expired_at: datetime | None
    sector_name: str | None
