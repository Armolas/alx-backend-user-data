#!/usr/bin/env python3
'''filter logger'''
import re


def filter_datum(fields, redaction, message, separator):
    '''filters a data and replaces a value'''
    for field in fields:
        pattern = fr'{field}=[^{separator}]*'
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message
