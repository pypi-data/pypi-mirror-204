""" Contains helper methods that aren't related directly to FFMPEG
"""
import ast
import random
import string
from typing import Any, Callable, Iterable, List, Optional, Set, Union


DOUBLE_QUOTE = '"'
LOG_FORMAT = "[%(levelname)s:%(funcName)s] %(message)s"


def ensureQuoted(s: str) -> str:
    """Ensures a string containing spaces is fully enclosed
    between double quotes
    """
    if " " not in s:
        return s
    res = s
    if s.startswith(DOUBLE_QUOTE):
        res = DOUBLE_QUOTE + res
    if s.endswith(DOUBLE_QUOTE):
        res = res + DOUBLE_QUOTE
    return res


def random_words(n: int, length: int, used_words: Set[str]) -> List[str]:
    """Generates random word (lowercase) of given length; if `used_words` is provided,
    it will avoid already-generated words
    """
    res: List[str] = []
    while len(res) < n:
        word = "".join(
            random.choice(string.ascii_lowercase) for _ in range(length)  # nosec B311
        )
        if used_words is not None:
            if word in used_words:
                continue
            used_words.add(word)
        res.append(word)
    return res
