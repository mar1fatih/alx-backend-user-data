#!/usr/bin/env python3
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        pattrn_text = ['{}=[^{}]+'.format(field, separator),
                       '{}={}'.format(field, redaction)]
        message = re.sub(pattrn_text[0], pattrn_text[1], message)
    return message
