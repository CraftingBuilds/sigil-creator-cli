import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sigil_creator.letters_to_numbers import convert, letter_value, reduce_to_digit
from sigil_creator.reduce_letters import reduce_intent


def test_reduce_intent_removes_vowels_and_duplicates():
    assert reduce_intent("I am the best", remove_vowels=True, keep_case=False) == "MTHBST"
    assert reduce_intent("Hello world", remove_vowels=False, keep_case=False) == "HELLOWRDL"


def test_letter_value_and_reduction():
    assert letter_value("A") == 1
    assert letter_value("z") == 26
    assert reduce_to_digit(26, max_val=9) == 8


def test_convert_reduces_numeric_sequence():
    assert convert("ABC") == [1, 2, 3]
    assert convert("Z", reduce=True) == [8]
    assert convert("abC", reduce=False) == [1, 2, 3]
