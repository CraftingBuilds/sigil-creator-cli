# sigil-creator

**CLI tools for creating personal magical sigils** grounded in classical Western occult traditions and modern chaos magic.

Implements the deterministic helper steps used by the [sigil-creator](https://github.com/example/sigil-creator) skill:

- Austin Osman Spare / chaos-magic letter reduction
- Letter → number conversion for Agrippa planetary kameas
- Visual **Sigil Profiles** (YAML) for consistent aesthetic rendering
- Method and kamea reference documents

The actual artistic construction of the glyph (overlapping strokes, path drawing on a magic square, image generation) is left to the practitioner or an external image model. This package supplies the reduction, numbering, style definitions, and documentation.

## Installation (Linux / macOS)

### From source (recommended while developing)

```bash
cd sigil-creator-cli
python3 -m pip install --user -e .
```

### Or build a wheel / sdist

```bash
python3 -m pip install build
python3 -m build
python3 -m pip install dist/sigil_creator-*.whl
```

After installation the following commands are available:

| Command            | Purpose                                      |
|--------------------|----------------------------------------------|
| `sigil`            | Main multi-command entry point               |
| `sigil-reduce`     | Stand-alone letter reducer                   |
| `sigil-numbers`    | Stand-alone letter→number converter          |

## Quick start

```bash
# 1. Reduce a Statement of Intent (Spare method)
sigil reduce "I am financially secure"
# → MFNCLYSR

# Keep vowels
sigil reduce --keep-vowels "I am financially secure"

# 2. Convert to kamea path numbers
sigil numbers MFNCLYSR
sigil numbers --max 7 "I am financially secure"

# 3. List / inspect visual profiles
sigil profiles
sigil show-profile antiquarian_calligraphic
sigil show-profile chaos_minimal

# 4. Read the full method reference
sigil methods
sigil methods --section Spare
sigil methods --section Kamea
sigil kameas

# 5. Concise workflow reminder
sigil guide
```

You can also pipe:

```bash
echo "It is my will to write every day" | sigil reduce
```

## Available Sigil Profiles

| ID                        | Character                                      |
|---------------------------|------------------------------------------------|
| `antiquarian_calligraphic`| Bold, archaic, interwoven, calligraphic        |
| `grimoire_engraved`       | Severe, angular, authoritative, plate-like     |
| `chaos_minimal`           | Clean, abstract, psychological, decisive       |
| `alchemical_manuscript`   | Ornate yet restrained, symbolic, manuscript    |

Profiles live in `sigil_creator/data/profiles/` and can be extended by dropping additional YAML files.

## Planetary Kameas (summary)

| Planet  | Square | Typical use                          |
|---------|--------|--------------------------------------|
| Saturn  | 3×3    | Protection, boundaries, endings      |
| Jupiter | 4×4    | Wealth, expansion, success           |
| Mars    | 5×5    | Energy, courage, conflict            |
| Sun     | 6×6    | Vitality, recognition, leadership    |
| Venus   | 7×7    | Love, beauty, harmony                |
| Mercury | 8×8    | Communication, intellect, commerce   |
| Moon    | 9×9    | Intuition, cycles, the subconscious  |

Full squares and reduction rules: `sigil kameas`.

## Charging & release (reminder)

1. Formulate a clear, present-tense, positive Statement of Intent.
2. Reduce / map it into an abstract mark.
3. Enter a state of gnosis (meditation, breath work, movement, etc.) while focusing on the sigil.
4. Deliberately forget the original desire so the unconscious can work.
5. Destroy, bury, or hide the physical sigil.

This package treats the practice as psychological technology, artistic craft, or sincere occult work according to the user’s own framework. It makes no claims about results.

## Development layout

```
sigil-creator-cli/
├── pyproject.toml
├── README.md
├── src/sigil_creator/
│   ├── __init__.py
│   ├── cli.py                 # main `sigil` command
│   ├── reduce_letters.py
│   ├── letters_to_numbers.py
│   └── data/
│       ├── profiles/          # YAML style definitions
│       └── references/        # methods.md, kameas.md
```

## License

MIT
