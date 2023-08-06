import re
from types import SimpleNamespace
from typing import Optional
from ..util import CHECK_DIGIT, validate_regexp
from .util import normalize


class MedicareNumber:
    """
    Australia medicare number format
    https://techdocs.broadcom.com/us/en/symantec-security-software/information-security/data-loss-prevention/15-8/about-data-loss-prevention-policies-v27576413-d327e9/library-of-system-data-identifiers-v95989112-d327e56315/australian-medicare-number-v115447646-d327e57399.html
    """
    METADATA = SimpleNamespace(**{
        'iso3166_alpha2': 'AU',
        # length without insignificant chars
        'min_length': 9,
        'max_length': 11,
        # has parse function
        'parsable': False,
        # has checksum function
        'checksum': True,
        # regular expression to validate the id
        'regexp': re.compile(r'^('
                             r'[2-6]\d{10}|[2-6]\d{3} \d{5} \d|[2-6]\d{3}-\d{5}-\d|'
                             r'[2-6]\d{9}|[2-6]\d{9}([-/]\d)?|'
                             r'[2-6]\d{3} \d{5} \d([-/]\d)?|[2-6]\d{3}-\d{5}-\d([-/]\d)?|'
                             r'[2-6]\d{3} \d{5} \d \d|[2-6]\d{3}-\d{5}-\d-\d'
                             r')$'),
        'alias_of': None,
        'names': ['Medicare Number', 'Medicare No'],
        'links': [
            'https://techdocs.broadcom.com/us/en/symantec-security-software/'
            'information-security/data-loss-prevention/15-8/'
            'about-data-loss-prevention-policies-v27576413-d327e9'
            '/library-of-system-data-identifiers-v95989112-d327e56315/'
            'australian-medicare-number-v115447646-d327e57399.html'],
        'deprecated': False
    })

    MAGIC_MULTIPLIER = [1, 3, 7, 9, 1, 3, 7, 9]
    """magic multiplier for checksum"""

    @staticmethod
    def validate(id_number: str) -> bool:
        """
        Validate the medicare number
        """
        if not validate_regexp(id_number, MedicareNumber.METADATA.regexp):
            return False
        normalized = normalize(id_number)
        checksum = MedicareNumber.checksum(id_number)
        return checksum is not None and checksum == int(normalized[8])

    @staticmethod
    def checksum(id_number: str) -> Optional[CHECK_DIGIT]:
        if not validate_regexp(id_number, MedicareNumber.METADATA.regexp):
            return None
        """algorithm: https://stackoverflow.com/questions/3589345/how-do-i-validate-an-australian-medicare-number."""
        normalized = normalize(id_number)
        # only validate first 8 digits
        number_list = [int(char) for char in list(normalized)][:8]
        total = sum([value * MedicareNumber.MAGIC_MULTIPLIER[index] for (index, value) in enumerate(number_list)])
        return total % 10
