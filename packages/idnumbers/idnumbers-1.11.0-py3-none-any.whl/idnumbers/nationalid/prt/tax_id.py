import re
from types import SimpleNamespace
from ..util import validate_regexp, weighted_modulus_digit


class TaxIDNumber:
    """
    Portugal Tax ID number
    Número de identificação fiscal or NIF
    https://en.wikipedia.org/wiki/National_identification_number#Portugal
    """
    METADATA = SimpleNamespace(**{
        'iso3166_alpha2': 'PT',
        # length without insignificant chars
        'min_length': 9,
        'max_length': 9,
        'parsable': False,
        'checksum': True,
        'regexp': re.compile(r'^([12356][0-9]|45|7[012]|9[0189])\d{7}$'),
        'alias_of': None,
        'names': ['Tax ID Number',
                  'Número de identificação fiscal'
                  'NIF'],
        'links': ['https://en.wikipedia.org/wiki/National_identification_number#Portugal'],
        'deprecated': False
    })

    @staticmethod
    def validate(id_number: str) -> bool:
        """
        Validate the Tax ID number
        https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/Portugal-TIN.pdf
        """
        return TaxIDNumber.checksum(id_number)

    @staticmethod
    def checksum(id_number: str) -> bool:
        """check the checksum"""
        if not validate_regexp(id_number, TaxIDNumber.METADATA.regexp):
            return False
        multipliers = [9, 8, 7, 6, 5, 4, 3, 2]
        mod = weighted_modulus_digit([int(i) for i in id_number[:-1]], multipliers, 11, True)
        calculated_checksum = 0 if mod == 0 or mod == 1 else (11 - mod)
        return calculated_checksum == int(id_number[-1])
