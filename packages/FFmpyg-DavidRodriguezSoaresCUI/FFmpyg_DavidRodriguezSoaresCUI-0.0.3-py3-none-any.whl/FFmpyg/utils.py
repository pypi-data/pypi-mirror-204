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


def assertTrue(condition: bool, message: str, *arguments) -> None:
    """Like assert, but without its optimization issues"""
    if not condition:
        raise AssertionError(message.format(*arguments))


def flatten_dict_join(d: dict) -> dict:
    """Returns a dictionnary with similar content but no nested dictionnary value
    WARNING: requires all keys to be str !
    Strategy to conserve key uniqueness is `key joining`:  d[k1][k2] -> d[k1.k2]
    """
    dflat = {}
    for k, v in d.items():
        assertTrue(isinstance(k, str), "Key {} is a {}, not str !", k, type(k))
        if isinstance(v, dict):
            d2 = flatten_dict_join(v)
            for k2, v2 in d2.items():
                assertTrue(
                    isinstance(k2, str), "Key {} is a {}, not str !", k2, type(k2)
                )
                k1_2 = k + "." + k2
                assertTrue(
                    k1_2 not in dflat, "Collision: key {} already in dict !", k1_2
                )
                dflat[k1_2] = v2
            continue

        assertTrue(k not in dflat, "Collision: key {} already in dict !", k)
        dflat[k] = v

    return dflat


def dict_difference(dictA: dict, dictB: dict) -> dict:
    """Performs dictA - dictB on the key-value pairs: Returns a dictionnary
    with all items from dictA minus the key-value pairs in common with dictB
    """
    diff = {
        k: dict_difference(v_a, dictB[k])
        if isinstance(v_a, dict) and k in dictB
        else v_a
        for k, v_a in dictA.items()
        if (k not in dictB) or (isinstance(v_a, dict) or v_a != dictB[k])
    }
    for k in list(diff.keys()):
        if diff[k] == {}:
            del diff[k]
    return diff


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


def user_input(
    prompt: str,
    accepted: Union[Iterable[Union[str, int]], Callable],
    default: Optional[Any] = None,
) -> Any:
    """Asks user for input, with restrictions on accpetable values.
    `prompt`: appropriate text asking the user for input. Should be straightforward and informative about the kind of data that is asked
    `accepted`: either a function testing if the user input is acceptable, or an iterable containing all acceptable values
    `default`: When given, if the user input is not acceptes, default is returned. When abscent, the user will be prompted again until either
    an accepted value is entered or a KeyboardInterrupt is raised.
    Note: this is only designed to retrieve values of the following types: str, int, float
    """

    # Smart prompt reformat
    if default is not None:
        prompt += f" [default:{default}] "
    if prompt[-1] == ":":
        prompt += " "
    elif prompt[-2:] != ": ":
        prompt += ": "

    def acceptable_UI(ui: Any) -> bool:
        return accepted(ui) if callable(accepted) else (ui in accepted)

    while True:
        # main loop: ask user until an acceptable input is received, or a KeyboradInterrupt ends the program
        _user_input = input(prompt)

        # case: raw user input is accepted
        if acceptable_UI(_user_input):
            return _user_input

        # case: processed user input is accepted
        variations = ["int(_user_input)", "float(_user_input)", "_user_input.lower()"]
        for variation in variations:
            try:
                __user_input = ast.literal_eval(variation)
                if acceptable_UI(__user_input):
                    return __user_input
            except (ValueError, AttributeError):
                pass

        # case: user input is not accepted AND there is a default
        if default is not None:
            return default

        # case: user input is not accepted AND there is no default => notify user, ask again
        print(
            "Input '%s' is not a valid input. %s",
            _user_input,
            (f"Please choose one of : {accepted}" if not callable(accepted) else ""),
        )


def choose_from_list(choices: list, default: Optional[int] = None) -> Any:
    """Prints then asks the user to choose an item from a list
    `default`
    """
    # Print choices
    print(
        "Choices:\n  "
        + "\n  ".join([f"[{idx}] {choice}" for idx, choice in enumerate(choices)])
        + "\n"
    )

    # Get user selection
    idx: int = user_input(
        "Selection : ", accepted=list(range(len(choices))), default=default
    )

    # Return choice
    return choices[idx]
