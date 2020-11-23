from random import random

def add_noise(s: str, bitrate: float) -> str:
    """Given a bit-string, flip ROUGHLY (bitrate*100) % of the bits

    Args:
        s: The input string
        pct: The percentage change of each bit being flipped

    Returns:
        str: A noisy string
    """
    out = ""
    for c in s:
        if not (c == "0" or c == "1"): 
            raise Exception(f"Invalid input: {s}. Must be a bit string.")

        if random() < bitrate:  # Flip the bit
            out += ("0" if c == "1" else "0")
        else:  # Don't flip the bit
            out += c

    return out

def hamming_encode(s: str, expected_bitrate: float, required_confidence: float) -> str:
    """Given a bit-string s, encode it with a hamming code

    TODO get rid of if/else; generalize
    """
    alpha = 0  # Calculate based off of expected bitrate and required confidence

    out = ""
    if delta > 0.5:  # Use [3, 1, 3] hamming code TODO 0.5 isn't right
        for c in s:
            out += c*3
    else:  # Use [7, 4, 3] hamming code
        raise Exception("Not implemented")

def hamming_decode(s):
    """Given a bit-string s, assume it was hamming encoded, and hamming decode it

    """
    if len(s) % 3 == 0:  # We used [3, 1, 3] encoding
        raise Exception("Not implemented")
    elif len(s) % 7 == 0:  # We used [7, 4, 3] encoding
        raise Exception("Not implemented")

print(add_noise("11010", 20))