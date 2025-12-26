from datetime import datetime

from schemas.camel_schema import CamelModelBase


class CustomerModelRes(CamelModelBase):
    id: str
    customer_name: str
    vat_number: str
    phone_number: str
    contact_name: str
    address: str
    city: str
    district: str
    country: str
    confirmed_at: datetime
    created_at: datetime
    expired_at: datetime
