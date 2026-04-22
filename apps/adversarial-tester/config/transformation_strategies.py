"""PyRIT-style transformation strategy metadata"""

# Canonical strategy definitions — keyed by legacy internal name.
# PyRIT canonical names are exposed as aliases (see PYRIT_STRATEGY_ALIASES below).
TRANSFORMATION_STRATEGIES: dict[str, dict[str, object]] = {
    "base64": {
        "name": "Base64 Encoding",
        "pyrit_name": "Base64",
        "description": "Encodes the harmful part of the query in Base64 with framing instructions",
        "encodes": "query",
        "category": "encoding",
    },
    "rot13": {
        "name": "ROT13 Encoding",
        "pyrit_name": "ROT13",
        "description": "Applies ROT13 Caesar cipher to the query",
        "encodes": "query",
        "category": "encoding",
    },
    "caesar": {
        "name": "Caesar Cipher",
        "pyrit_name": "Caesar",
        "description": "Applies a Caesar cipher shift to the query",
        "encodes": "query",
        "category": "encoding",
        "shift": 13,
    },
    "leetspeak": {
        "name": "Leetspeak Substitution",
        "pyrit_name": "Leetspeak",
        "description": "Replaces characters with leet equivalents (a→4, e→3, i→1, o→0, s→5, t→7)",
        "encodes": "query",
        "category": "substitution",
    },
    "flip": {
        "name": "Character Flip",
        "pyrit_name": "Flip",
        "description": "Reverses character order in the query",
        "encodes": "query",
        "category": "obfuscation",
    },
    "char_swap": {
        "name": "Character Swap",
        "pyrit_name": "CharSwap",
        "description": "Swaps adjacent character pairs in the query",
        "encodes": "query",
        "category": "obfuscation",
    },
    "unicode_sub": {
        "name": "Unicode Substitution",
        "pyrit_name": "UnicodeConfusable",
        "description": "Replaces Latin characters with visually similar Unicode lookalikes",
        "encodes": "query",
        "category": "substitution",
    },
    "suffix_append": {
        "name": "Jailbreak Suffix",
        "pyrit_name": "SuffixAppend",
        "description": "Appends a standard AIM/DAN-style jailbreak suffix to the query",
        "encodes": "query",
        "category": "jailbreak",
    },
    "char_space": {
        "name": "Character Spacing",
        "pyrit_name": "CharacterSpace",
        "description": "Inserts spaces between characters to evade keyword detection",
        "encodes": "query",
        "category": "obfuscation",
    },
}

# Mapping from PyRIT canonical name → legacy internal key.
# Used to accept PyRIT names in API requests while keeping existing behaviour.
PYRIT_STRATEGY_ALIASES: dict[str, str] = {
    v["pyrit_name"]: k  # type: ignore[index]
    for k, v in TRANSFORMATION_STRATEGIES.items()
}


def resolve_strategy_key(name: str) -> str:
    """Return the internal strategy key for *name*.

    Accepts both the legacy internal key (e.g. ``"base64"``) and the PyRIT
    canonical name (e.g. ``"Base64"``).  Returns the internal key unchanged if
    no alias match is found so that unrecognised values surface as errors at
    call sites.
    """
    return PYRIT_STRATEGY_ALIASES.get(name, name)
