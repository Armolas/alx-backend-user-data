#!/usr/bin/env python3
'''filter logger'''
import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    '''filters a data and replaces a value'''
    for field in fields:
        pattern = fr'{field}=[^{separator}]*'
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message
