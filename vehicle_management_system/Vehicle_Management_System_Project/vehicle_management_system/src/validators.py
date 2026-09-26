import re


def require_text(value, field):
    value = value.strip()
    if not value:
        raise ValueError(f"{field} cannot be empty.")
    return value


def validate_phone(phone):
    phone = phone.strip()
    if not re.fullmatch(r"[0-9]{10}", phone):
        raise ValueError("Phone must contain exactly 10 digits.")
    return phone


def validate_year(year):
    if year < 1900 or year > 2100:
        raise ValueError("Year must be between 1900 and 2100.")
    return year


def validate_rate(rate):
    if rate <= 0:
        raise ValueError("Daily rate must be greater than zero.")
    return rate


def validate_days(days):
    if days <= 0:
        raise ValueError("Number of days must be greater than zero.")
    return days
