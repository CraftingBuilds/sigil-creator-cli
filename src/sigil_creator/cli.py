#!/usr/bin/env python3
"""Main entry point for the sigil-creator CLI."""

from __future__ import annotations

import argparse
import importlib.resources as resources
import sys
from pathlib import Path
from typing import Optional

from . import __version__
from .reduce_letters import reduce_intent
from .letters_to_numbers import convert


def get_data_path(relative: str) -> Path:
    """Locate package data files (profiles, references)."""
    try:
        # Python 3.9+
        base = resources.files("sigil_creator")
        return Path(str(base.joinpath("data", relative)))
    except Exception:
        # Fallback for development / editable installs
        here = Path(__file__).resolve().parent
        return here / "data" / relative


def cmd_reduce(args: argparse.Namespace) -> int:
    text = args.intent or sys.stdin.read()
    if not text.strip():
        print("Error: provide a statement of intent as argument or on stdin.", file=sys.stderr)
        return 1
    result = reduce_intent(
        text.strip(),
        remove_vowels=not args.keep_vowels,
        keep_case=args.keep_case,
    )
    print(result)
    return 0


def cmd_numbers(args: argparse.Namespace) -> int:
    text = args.text or sys.stdin.read()
    if not text.strip():
        print("Error: provide letters or intent as argument or on stdin.", file=sys.stderr)
        return 1
    numbers = convert(text, reduce=not args.no_reduce, max_val=args.max)
    print(" ".join(map(str, numbers)))
    if args.verbose:
        print(f"Sequence: {numbers}", file=sys.stderr)
    return 0


def cmd_profiles(args: argparse.Namespace) -> int:
    profiles_dir = get_data_path("profiles")
    if not profiles_dir.is_dir():
        print(f"Profiles directory not found: {profiles_dir}", file=sys.stderr)
        return 1
    files = sorted(profiles_dir.glob("*.yaml"))
    if not files:
        print("No profiles found.")
        return 0
    for f in files:
        print(f.stem)
        if args.verbose:
            print(f"  → {f}")
    return 0


def cmd_show_profile(args: argparse.Namespace) -> int:
    path = get_data_path(f"profiles/{args.name}.yaml")
    if not path.is_file():
        # try without extension / fuzzy
        candidates = list(get_data_path("profiles").glob(f"*{args.name}*.yaml"))
        if len(candidates) == 1:
            path = candidates[0]
        else:
            print(f"Profile not found: {args.name}", file=sys.stderr)
            print("Available:", file=sys.stderr)
            for p in sorted(get_data_path("profiles").glob("*.yaml")):
                print(f"  {p.stem}", file=sys.stderr)
            return 1
    print(path.read_text(encoding="utf-8"))
    return 0


def cmd_methods(args: argparse.Namespace) -> int:
    path = get_data_path("references/methods.md")
    if not path.is_file():
        print(f"Reference not found: {path}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    if args.section:
        # Simple section filter
        lines = text.splitlines()
        out = []
        capturing = False
        for line in lines:
            if line.startswith("## ") and args.section.lower() in line.lower():
                capturing = True
            elif line.startswith("## ") and capturing:
                break
            if capturing:
                out.append(line)
        print("\n".join(out) if out else text)
    else:
        print(text)
    return 0


def cmd_kameas(args: argparse.Namespace) -> int:
    path = get_data_path("references/kameas.md")
    if not path.is_file():
        print(f"Reference not found: {path}", file=sys.stderr)
        return 1
    print(path.read_text(encoding="utf-8"))
    return 0


def cmd_guide(args: argparse.Namespace) -> int:
    """Print a concise practical guide for creating a sigil from the CLI."""
    guide = f"""
sigil-creator {__version__} — Quick Guide
========================================

1. Formulate a Statement of Intent (SoI)
   Present tense, positive, specific, already-true:
     "I am financially secure"
     "It is my will to find steady creative work I enjoy"

2. Reduce the letters (Spare / chaos method — default)
   $ sigil reduce "I am financially secure"
   → MFNCLYSR   (vowels removed, unique letters)

   Keep vowels:
   $ sigil reduce --keep-vowels "I am financially secure"

3. Convert to numbers for a planetary kamea
   $ sigil numbers MFNCLYSR
   $ sigil numbers --max 9 "I am financially secure"

4. Choose a visual profile
   $ sigil profiles
   $ sigil show-profile antiquarian_calligraphic

5. Read method details
   $ sigil methods
   $ sigil methods --section Spare
   $ sigil kameas

6. Construct the glyph yourself (or with an image model)
   - Overlap / rotate / share strokes of the reduced letters
   - For kamea: plot the number sequence as a path on the chosen square
     (start with open circle, end with a bar)
   - Apply the stroke, geometry and composition rules from the chosen profile

7. Charge & release
   Enter gnosis (meditation, breath, movement, etc.), gaze, then deliberately
   forget the original desire. Destroy or hide the physical mark.

Full references are shipped with the package under the data/ tree.
"""
    print(guide.strip())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sigil",
        description="Create personal magical sigils — letter reduction, kamea numbers, profiles & references.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  sigil reduce \"I am calm and focused\"\n"
               "  sigil numbers --max 7 ABCDEF\n"
               "  sigil profiles\n"
               "  sigil show-profile chaos_minimal\n"
               "  sigil methods --section Kamea\n"
               "  sigil guide\n",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    sub = parser.add_subparsers(dest="command", required=True)

    # reduce
    p_reduce = sub.add_parser("reduce", help="Reduce a statement of intent to unique letters (Spare method)")
    p_reduce.add_argument("intent", nargs="?", help="Statement of intent (or read from stdin)")
    p_reduce.add_argument("--keep-vowels", action="store_true", help="Do not strip vowels")
    p_reduce.add_argument("--keep-case", action="store_true", help="Preserve original case")
    p_reduce.set_defaults(func=cmd_reduce)

    # numbers
    p_num = sub.add_parser("numbers", help="Convert letters to numbers for kamea paths")
    p_num.add_argument("text", nargs="?", help="Letters or full intent (or stdin)")
    p_num.add_argument("--no-reduce", action="store_true", help="Do not digital-root reduce")
    p_num.add_argument("--max", type=int, default=9, help="Maximum value after reduction (default 9)")
    p_num.add_argument("-v", "--verbose", action="store_true")
    p_num.set_defaults(func=cmd_numbers)

    # profiles
    p_prof = sub.add_parser("profiles", help="List available visual Sigil Profiles")
    p_prof.add_argument("-v", "--verbose", action="store_true")
    p_prof.set_defaults(func=cmd_profiles)

    # show-profile
    p_show = sub.add_parser("show-profile", help="Print a profile YAML definition")
    p_show.add_argument("name", help="Profile id (e.g. antiquarian_calligraphic)")
    p_show.set_defaults(func=cmd_show_profile)

    # methods
    p_meth = sub.add_parser("methods", help="Show detailed method reference")
    p_meth.add_argument("--section", "-s", help="Filter to a section title (Spare, Kamea, Rose, Grimoire…)")
    p_meth.set_defaults(func=cmd_methods)

    # kameas
    p_kam = sub.add_parser("kameas", help="Show Agrippa planetary magic squares reference")
    p_kam.set_defaults(func=cmd_kameas)

    # guide
    p_guide = sub.add_parser("guide", help="Print a short practical workflow guide")
    p_guide.set_defaults(func=cmd_guide)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
