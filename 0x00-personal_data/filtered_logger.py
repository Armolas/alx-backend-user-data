#!/usr/bin/env python3
'''filter logger'''
import logging
import mysql.connector
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

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''returns a cursor to a database'''
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME', 'holberton')

    try:
        db_connector = mysql.connector.connect(
                user=user,
                password=password,
                host=host,
                database=db
                )
        return db_connector
    except mysql.connector.Error as err:
        return None


def main():
    '''Main function'''
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    users = []
    for row in cursor:
        users.append(f"name={row[0]}; email={row[1]}; phone={row[2]}; \
ssn={row[3]}; password={row[4]}; ip={row[5]}; \
last_login={row[6]}; user_agent={row[7]};")
    cursor.close()
    db.close()
    for message in users:
        log_record = logging.LogRecord(
                "my_logger",
                logging.INFO,
                None,
                None,
                message,
                None,
                None
                )
        formatter = RedactingFormatter(
                fields=("email", "ssn", "password", "name", "phone")
                )
        print(formatter.format(log_record))


if __name__ == '__main__':
    main()
