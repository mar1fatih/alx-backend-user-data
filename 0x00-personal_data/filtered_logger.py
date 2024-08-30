#!/usr/bin/env python3
"""filter_datum"""
import re
import logging
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        pattrn_text = ['{}=[^{}]+'.format(field, separator),
                       '{}={}'.format(field, redaction)]
        message = re.sub(pattrn_text[0], pattrn_text[1], message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ class constructor """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ format method to obfuscated message """
        n = filter_datum(self.fields, self.REDACTION,
                         super(RedactingFormatter, self).format(record),
                         self.SEPARATOR)
        return n


def get_logger() -> logging.Logger:
    """ get logger method """
    user = logging.getLogger('user_data')
    user.setLevel(logging.INFO)
    user.propagate = False
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter(PII_FIELDS))
    user.addHandler(stream)
    return user
