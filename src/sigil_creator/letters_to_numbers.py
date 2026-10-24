#!/usr/bin/env python3
"""Convert letters to numbers for kamea sigil paths. Simple A=1..Z=26 with optional reduction."""

import sys
import argparse

def letter_value(c: str) -> int:
    c = c.upper()
    if not c.isalpha():
        return 0
    return ord(c) - ord('A') + 1

def reduce_to_digit(n: int, max_val: int = 9) -> int:
    while n > max_val:
        n = sum(int(d) for d in str(n))
    return n if n > 0 else 9  # avoid 0

def convert(text: str, reduce: bool = True, max_val: int = 9) -> list:
    vals = []
    for c in text:
        if c.isalpha():
            v = letter_value(c)
            if reduce:
                v = reduce_to_digit(v, max_val)
            vals.append(v)
    return vals

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", nargs="?", help="Letters or intent")
    parser.add_argument("--no-reduce", action="store_true")
    parser.add_argument("--max", type=int, default=9, help="Max value for reduction (square size related)")
    args = parser.parse_args()
    
    text = args.text or sys.stdin.read().strip()
    # Simple: just convert letters present
    numbers = convert(text, reduce=not args.no_reduce, max_val=args.max)
    print(" ".join(map(str, numbers)))
    print("Sequence:", numbers)

if __name__ == "__main__":
    main()
