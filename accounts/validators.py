import re

from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


def is_valid_national_code(value):
    if not re.search(r'^\d{10}$', value):
        raise ValidationError(_('The entered National_ID is not 10 digits'))
    else:
        check = int(value[9])
        s = sum([int(value[x]) * (10 - x) for x in range(9)]) % 11
        if (2 > s == check) or (s >= 2 and check + s == 11):
            return True
        else:
            raise ValidationError(_('Please enter a valid National_ID'))


class NumericPasswordValidator:
    def validate(self, password, user=None):
        if not password.isdigit() or len(password) != 6:
            raise ValidationError(
                _("Password must be a 6-digit number."),
                code='password_not_numeric'
            )

    def get_help_text(self):
        return _(
            "Your password must be a 6-digit number."
        )
