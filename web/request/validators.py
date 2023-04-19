import phonenumbers


def phone_number_must_be_valid(number: str) -> str:
    try:
        phone = phonenumbers.parse(number)
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValueError("Value is not a phone number")
    if not phonenumbers.is_valid_number(phone):
        raise ValueError("Invalid phone number")
    return number
