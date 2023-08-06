import re
from types import SimpleNamespace

from ..util import validate_regexp


class SocialSecurityNumber:
    """
    San Marino, individual social security number, SSI number
    https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/San-Marino-TIN.pdf
    """
    METADATA = SimpleNamespace(**{
        'iso3166_alpha2': 'SM',
        'min_length': 9,
        'max_length': 9,
        # length without insignificant chars
        'parsable': False,
        # has parse function
        'checksum': False,
        # has checksum function
        'regexp': re.compile(r'^\d{9}$'),
        # regular expression to validate the id
        'alias_of': None,
        'names': ['Social Security Number',
                  'SSI'],
        'links': ['https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/'
                  'tax-identification-numbers/San-Marino-TIN.pdf'],
        'deprecated': False
    })

    @staticmethod
    def validate(id_number: str) -> bool:
        """
        Validate
        """
        return validate_regexp(id_number, SocialSecurityNumber.METADATA.regexp)


SSI = SocialSecurityNumber
"""alias of SocialSecurityNumber"""
