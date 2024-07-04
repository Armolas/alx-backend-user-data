#!/usr/bin/env python3
'''filter logger'''
import logging
import mysql.connector
from mysql.connector import connection
import os
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


PII_FIELDS = ("email", "phone", "ssn", "password", "name")


def get_logger() -> logging.Logger:
    '''Returns a logger object'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    ch = logging.StreanHandler()
    ch.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def get_db() -> connection.MySQLConnection:
    '''returns a cursor to a database'''
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=db
            )
