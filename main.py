# Imports

import numpy as np

# Constants
# G = 
# H = np.linalg.solve(G, np.zeros(7, 7), dtype=int)
# H_t = np.transpose(H)

G_standard = np.array([  # np.linalg.solve(H_t_standard, np.zeros((4, 3), dtype=int))
    [0, 1, 1, 1, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 0],
    [1, 1, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 0, 0, 1]
])

H_standard = np.array([
    [1, 0, 0, 0, 1, 1, 1],
    [0, 1, 0, 1, 0, 1, 1],
    [0, 0, 1, 1, 1, 0, 1],
])

H_t_standard = np.transpose(H_standard)

decode_standard = np.array([
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])

standard_syndrome_lookup = {  # key:value = syndrome:bit_position
    (0, 0, 0): 0,
    (0, 0, 1): 3,
    (0, 1, 0): 2,
    (0, 1, 1): 4,
    (1, 0, 0): 1,
    (1, 0, 1): 5,
    (1, 1, 0): 6,
    (1, 1, 1): 7,
}


def hamming_encode_743(message: np.ndarray, standard: bool = False) -> np.ndarray:
    """Given a 4 bit message, encode it as a 7 bit hamming code.

    :param np.ndarray message: A 4 bit message to encode, as an ndarray of shape (4,)
    :param bool standard: Use the standard form of G and H (defaults to ``False``)
    
    :rtype: np.ndarray
    :returns: The encoded message, as an ndarray of shape (7,)
    """
    if message.shape != (4,):
        raise Exception(f"hamming_encode_743 expects a vector of size (4,), not {message.shape}")

    g = G_standard if standard else G

    encoded = np.mod(message @ g, 2)  # matrix multiplication, mod 2
    return encoded

def hamming_decode_743(received: np.ndarray, standard: bool = False) -> np.ndarray:
    """Given a 7 bit code, decode it to a 4 bit message.

    :param np.ndarray received: A 7 bit received code, as an ndarray of shape (7,)
    :param bool standard: Use the standard form of G and H (defaults to ``False``)
    
    :rtype: np.ndarray
    :returns: The decoded message, as an ndarray of shape (4,)
    """
    if received.shape != (7,):
        raise Exception(f"hamming_decode_743 expects a vector of size (7,), not {message.shape}")

    h_t = H_t_standard if standard else H_t

    syndrome = np.mod(received @ h_t, 2)
    print(f"syndrome: {syndrome}")
    corrected = _correct_743(received=received, syndrome=syndrome, standard=standard)
    print(f"fixed code word: {corrected}")

    return _undo_encoding_743(corrected=corrected, standard=standard)

def _correct_743(received: np.ndarray, syndrome: np.ndarray, standard: bool) -> np.ndarray:
    """Given a 7 bit code and a syndrome, return the corrected 7 bit code.

    :param np.ndarray received: A 7 bit received message of shape (7,)
    :param np.ndarray syndrome: A 3 bit calculated syndrome of shape (3,)
    :param bool standard: Use the standard form of G and H (defaults to ``False``)
    
    :rtype: np.ndarray
    :returns: The corrected, encoded message, as an ndarray of shape (7,)
    """
    if standard:
        position = standard_syndrome_lookup[tuple(syndrome)]
        if position == 0:  # No error found
            return received
        else:
            np.put(received, position - 1, (1 - received[position - 1]))
            return received
    else:
        raise Exception("Not supported yet!")

def _undo_encoding_743(corrected: np.ndarray, standard: bool = False):
    """Given a (fixed) codeword, undo its encoding back to a 4 bit array

    :param np.ndarray codeword: A shape (7,) codeword

    :rtype: np.ndarray
    :returns: The decoded message
    """
    d = decode_standard if standard else decode
    return np.mod(corrected @ d, 2)


ex = np.array([0, 1, 1, 0])
err = np.array([0, 0, 0, 0, 0, 1, 0])
print(f"message: {ex}")
encoded = hamming_encode_743(ex, standard=True)
print(f"code word: {encoded}")
message = np.mod(encoded + err, 2)
print(f"noisy code word: {message}")
decoded_message = hamming_decode_743(message, standard=True)
print(f"decoded message: {decoded_message}")
