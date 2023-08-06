def boolean_validator(field, value, error):
    if value and value not in ["true", "false"]:
        error(field, "Must be a boolean value: true or false")


S_ADDRESS_CREATE = {
    "street": {"type": "string", "required": True, "empty": False},
    "zip_code": {"type": "string", "required": True, "empty": False},
    "city": {"type": "string", "required": True, "empty": False},
    "country": {"type": "string", "required": True, "empty": False}
}

S_SUBSCRIPTION_REQUEST_CREATE_FIELDS = {
    "iban": {"type": "string", "required": True},
    "vat": {"type": "string", "required": True},
    "address": {"type": "dict", "schema": S_ADDRESS_CREATE},
    "phone": {"type": "string"},
    "firstname": {"type": "string"},
    "lastname": {"type": "string"},
    "email": {"type": "string"},
    "lang": {"type": "string"},
    "is_company": {"type": "boolean"},
    "ordered_parts": {"type": "integer"},
    "share_product_id": {"type": "integer"},
}
