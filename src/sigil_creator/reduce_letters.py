#!/usr/bin/env python3
"""Reduce a statement of intent to unique letters for Spare-style sigil creation."""

import sys
import argparse

def reduce_intent(text: str, remove_vowels: bool = True, keep_case: bool = False) -> str:
    text = text.upper() if not keep_case else text
    # Keep only letters
    letters = [c for c in text if c.isalpha()]
    if remove_vowels:
        vowels = set("AEIOU")
        letters = [c for c in letters if c not in vowels]
    seen = set()
    unique = []
    for c in letters:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    return "".join(unique)

def main():
    parser = argparse.ArgumentParser(description="Reduce intent statement for sigil creation")
    parser.add_argument("intent", nargs="?", help="Statement of intent")
    parser.add_argument("--keep-vowels", action="store_true", help="Do not remove vowels")
    parser.add_argument("--keep-case", action="store_true", help="Preserve original case")
    args = parser.parse_args()
    
    if args.intent:
        result = reduce_intent(args.intent, remove_vowels=not args.keep_vowels, keep_case=args.keep_case)
        print(result)
    else:
        # Interactive or stdin
        for line in sys.stdin:
            result = reduce_intent(line.strip(), remove_vowels=not args.keep_vowels, keep_case=args.keep_case)
            print(result)

if __name__ == "__main__":
    main()
