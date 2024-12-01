import sys
import argparse
import hashlib
import re

# https://github.com/trezor/python-mnemonic
# pip install mnemonic
from mnemonic import Mnemonic

# Language for mnemonic
LANGUAGE = "english"
mn = Mnemonic(LANGUAGE)

HELP_STRING = """
Convert between BIP39 mnemonic phrases, hex strings, and plain text.

You will be prompted for input text.
- If input is a hex string, convert to BIP39 mnemonic phrase.
- If input is a BIP39 mnemonic phrase, convert to hex string.
- If input is a plain text string, convert to hex string.

Output is always the sha256 hash and the bip39 mnemonic phrase.
"""

# Map from valid BIP39 word lengths to the number of bytes they represent.
WORDS_TO_BYTES = {
    12: 16,
    15: 20,
    18: 24,
    21: 28,
    24: 32,
}


def normalize_string(s: str) -> str:
    """Normalize a string by
    - removing leading and trailing spaces from each line
    - making all characters lowercase
    - combining muliple lines into one
    """

    # Remove leading and trailing spaces from each line and convert to lowercase.
    s = s.strip().lower()

    # Combine multiple lines into one.
    s = " ".join([x.strip() for x in s.splitlines()])

    # Remove extra spaces between words.
    s = re.sub(r"\s+", " ", s)

    return s


def is_hex(s: str) -> bool:
    """Returns true if the string is a hex string, false otherwise."""

    s = normalize_string(s)

    try:
        b = bytes.fromhex(s)
        return len(b) in WORDS_TO_BYTES.values()
    except ValueError:
        return False


def is_bip39(s: str, lang: str = LANGUAGE) -> bool:
    """Returns true if the string is a bip39 string, false otherwise."""

    s = normalize_string(s)

    try:
        mn = Mnemonic(lang)
        mn.to_entropy(s)
        return True
    except ValueError:
        return False


def get_multiline_input(prompt="Enter text (end with Ctrl+D on Unix or Ctrl+Z on Windows):\n"):
    print(prompt, end="")
    return sys.stdin.read()


def print_it(sha256_hash: str, bip39_words: str):
    print(f"[{len(sha256_hash)}, {len(bip39_words.split())}]")
    print(sha256_hash.hex())

    tokens = bip39_words.split()
    idx = [hex(mn.wordlist.index(t))[-1] for t in tokens]

    print(bip39_words)
    print("-".join(tokens[:3]) + "-" + "".join(idx[-4:]))


def main():
    parser = argparse.ArgumentParser(
        description=HELP_STRING,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    args = parser.parse_args()

    input_text = get_multiline_input()
    input_text = input_text.strip()
    print()

    sha256_hash = None
    bip39_words = None

    # Get the sha256 bytes for the input.
    input_type = "OTHER"
    if is_hex(input_text):
        input_type = "HEX"
        sha256_hash = bytes.fromhex(normalize_string(input_text))

    elif is_bip39(input_text):
        input_type = "BIP39"
        bip39_words = normalize_string(input_text)
        sha256_hash = mn.to_entropy(bip39_words)

    if input_type == "OTHER":
        sha256_hash = hashlib.sha256(input_text.encode()).digest()

    # Iterate over different slices of sha256 bytes and generaete bip39 phrases.
    print(f"=== {input_type} ===")
    for hash_len in sorted(WORDS_TO_BYTES.values(), reverse=True):
        if hash_len > len(sha256_hash):
            continue

        hash_start = len(sha256_hash) - hash_len
        if hash_start < 0:
            continue
        new_hash = sha256_hash[hash_start:]
        print_it(new_hash, mn.to_mnemonic(new_hash))
        print()


if __name__ == "__main__":
    main()
