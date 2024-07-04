#!/usr/bin/env python3
'''filter logger'''
import logging
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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''formats the record message'''
        record.msg = filter_datum(
                self.fields,
                self.REDACTION,
                record.msg,
                self.SEPARATOR
                )
        return super(RedactingFormatter, self).format(record)
