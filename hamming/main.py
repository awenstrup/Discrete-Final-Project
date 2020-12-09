# Imports
import random
import numpy as np
from bitarray import bitarray as ba

# Constants
G = []
H = []
H_t = []

G_standard = np.array([
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

def encode(s: str) -> np.ndarray:
    """Given a string, encode it as an array of hamming codes.

    :param str s: The input string

    :rtype: numpy.ndarray
    :returns: A 2D array, which is an array of 7-bit codewords (each codeword is itself an array)

    Steps:
        1. A string is first converted to bits using utf-8
        2. A bitstring is converted to a 4xn array of 4-bit messages
        3. Each 4 bit message is converted to a codeword using the hamming (7, 4, 3) encoding
    """
    # Convert to bitarray
    b = bytes(s, "utf-8")
    bits = ba()
    bits.frombytes(b)

    # Convert to ndarray of size (4, n)
    flat_array = np.frombuffer(bits.unpack(), dtype=bool).astype(int)  # ik this is weird, i think i need it
    array = flat_array.reshape(4, int(len(flat_array)/4), order='F').T

    # Encode each 4 bit message
    out = list()
    for message in array:
        out.append(list(encode_743(message)))

    return np.array(out)

def add_noise(message: np.ndarray, erate: float, cleanly: bool = False) -> None:
    """Alter a message in place, flipping about erate*100 % of the bits

    :param np.ndarray message: The message to add noise to
    :param float erate: What portion of the bits to flip. Specify a float between 0 and 1
    :param bool cleanly: Option to flip at most 1 bit per 7 bit codeword. Guarantees message
        will always be decodable. 

    :rtype: None
    :returns: Nothing

    """
    shape = message.shape
    for i in range(shape[0] - 1):
        for j in range(shape[1] - 1):
            if random.random() < erate:
                message[i][j] = 0 if message[i][j] == 1 else 1
                # print(f"Error injected at i: {i}, j: {j}")
                if cleanly:
                    break
 

def decode(received: np.ndarray) -> str:
    """Given an list of 7-bit codewords, decode to a string.

    :param numpy.ndarray s: The array of codewords, as a 7xn numpy ndarray

    :rtype: str
    :returns: The decoded string

    Steps (opposite from encode):
        1. Each 7 bit codeword is converted to a message using the hamming (7, 4, 3) decoding
        2. The numpy ndarray is flattened to a bitstring
        3. The bitstring is converted back to a string, using utf-8
    """
    # Decode all the codewords
    decoded = list()
    for code in received:
        decoded.append(decode_743(code))

    # Convert to string
    flattened: np.ndarray = np.array(decoded).flatten()
    bits: ba = ba(list(flattened))
    b: bytes = ba.tobytes(bits)
    out: str = b.decode("utf-8")

    return out


def encode_743(message: np.ndarray, standard: bool = True) -> np.ndarray:
    """Given a 4 bit message, encode it as a 7 bit hamming code.

    :param np.ndarray message: A 4 bit message to encode, as an ndarray of shape (4,)
    :param bool standard: Use the standard form of G and H (defaults to ``False``)
    
    :rtype: np.ndarray
    :returns: The encoded message, as an ndarray of shape (7,)
    """
    try:
        message = np.array(message)
    except:
        raise Exception(f"Could not decode message {message}; could not convert to numpy.ndarray.")

    if message.shape != (4,):
        raise Exception(f"hamming_encode_743 expects a vector of size (4,), not {message.shape}")

    g = G_standard if standard else G

    encoded = np.mod(message @ g, 2)  # matrix multiplication, mod 2
    return encoded

def decode_743(received: np.ndarray, standard: bool = True) -> np.ndarray:
    """Given a 7 bit code, decode it to a 4 bit message.

    :param np.ndarray received: A 7 bit received code, as an ndarray of shape (7,)
    :param bool standard: Use the standard form of G and H (defaults to ``False``)
    
    :rtype: np.ndarray
    :returns: The decoded message, as an ndarray of shape (4,)
    """
    try:
        received = np.array(received)
    except:
        raise Exception(f"Could not decode message {received}; could not convert to numpy.ndarray.")

    if received.shape != (7,):
        raise Exception(f"hamming_decode_743 expects a vector of size (7,), not {message.shape}")

    h_t = H_t_standard if standard else H_t

    syndrome = np.mod(received @ h_t, 2)
    # print(f"syndrome: {syndrome}")
    corrected = _correct_743(received=received, syndrome=syndrome, standard=standard)
    # print(f"fixed code word: {corrected}")

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


if __name__ == "__main__":
    ex = np.array([0, 1, 1, 0])
    err = np.array([0, 0, 0, 0, 0, 1, 0])
    print(f"message: {ex}")
    encoded = encode_743(ex, standard=True)
    print(f"code word: {encoded}")
    message = np.mod(encoded + err, 2)
    print(f"noisy code word: {message}")
    decoded_message = decode_743(message, standard=True)
    print(f"decoded message: {decoded_message}")
