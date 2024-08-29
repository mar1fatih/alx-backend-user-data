#!/usr/bin/env python3
"""filter_datum"""
import re
import logging
from typing import List


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

    def __init__(self, fields):
        """ constructor """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ format method to obfuscated message """
        n = filter_datum(self.fields, self.REDACTION,
                         logging.Formatter.format(self, record=record),
                         self.SEPARATOR)
        return n
