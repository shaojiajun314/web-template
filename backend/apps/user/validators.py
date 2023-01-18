from django.core.exceptions import ValidationError


def is_username_validator(value):
    try:
        int(value)
    except ValueError:
        return
    raise ValidationError('''账号不允许为纯数字''')
