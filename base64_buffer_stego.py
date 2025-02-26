from base64 import b64encode
from typing import TextIO

base64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
dict = [x for x in base64_alphabet]
padding_bits = ""


def get_message(padding_bits: str | TextIO) -> str:
    """
    This function will take a string of padding bits and return the message.
    The first 16 bits of the padding bits will be the size of the message.
    """
    size = int(padding_bits[:16], 2) * 7
    bin_message = padding_bits[16: 16 + size]
    print(size, len(bin_message))

    return "".join(chr(int(bin_message[i: i + 7], 2)) for i in range(0, len(bin_message), 7))


def base64_padding_decoder(base64_strings: str) -> str:
    """
    This function will take a list of base64 strings and return the padding bits
    :param base64_strings: This is a newline separated list of base64 strings
    :return: A string decoded from the padding bits
    """
    output = ""
    for line in base64_strings.split("\n"):
        binary_line = ""
        # print(line, end=" " )
        for letter in line.strip():
            if letter in base64_alphabet:
                number = base64_alphabet.index(letter)
                bin_number = bin(number).replace("0b", "").zfill(6)
                binary_line += bin_number
        padding_characters = len(binary_line) % 8
        if padding_characters != 0:
            # print(line, binary_line[-padding_characters:], padding_characters, len(binary_line), end=" ")
            output += binary_line[-padding_characters:]
    # print()
    return get_message(output)


def encode_word(word, secret):
    """Encode 2 or 4 bits of secret inside base64 encoded word

    Arguments:
    word (str)           -- Base64 encoded word serving as carrier
    secret (str)         -- 2-bit or 4-bit secret to hide

    Output:
    encoded_string (str) -- Re-encoded base64 string with secret
    """
    first_equal = word.index('=')
    to_modify = word[first_equal - 1]
    delta = int(secret, 2)
    encoded_char = dict[dict.index(to_modify) + delta]
    encoded_string = word[:first_equal - 1] + encoded_char + (len(word) - first_equal) * '='
    return encoded_string


def count_equals(word_list):
    """Returns the number of bits that can be hidden inside a text

    Arguments:
    word_list (str[]) -- List of Base64 strings

    Output:
    count (int)       -- Number of '=' in the list times 2
    """
    equals = 0
    for word in word_list:
        equals += word.count('=')
    count = 2 * equals
    return count


def encode(text, secret):
    """Encodes a secret in a base64 word list, from a text string

    Arguments:
    text (str)           -- ascii text serving as a carrier
    secret (str)         -- secret ascii text to encode of max length 2^16 words
    verbose (bool)       -- verbosity toggle

    Output:
    encoded_list (str[]) -- base64 list of words with the secret encoded within
    """
    words = text.split(' ')
    words_b64 = [b64encode((word + " ").encode('ascii')).decode('ascii') for word in words]
    secret_max_length = count_equals(words_b64)

    if 7 * len(secret) + 16 > secret_max_length:
        raise ValueError('[ERROR] The text size is too small for the secret. Please add more text.')

    bin_secret = bin(len(secret))[2:].zfill(16)
    for char in secret:
        bin_secret += bin(ord(char))[2:].zfill(7)
    bin_secret = bin_secret + (secret_max_length - len(bin_secret)) * '0'
    encoded_list = []
    for word in words_b64:
        equals = word.count('=')
        if equals > 0:
            encoded_list.append(encode_word(word, bin_secret[:2 * equals]))
            bin_secret = bin_secret[2 * equals:]
        else:
            encoded_list.append(word)
    return encoded_list


def open_file(filename: str):
    with open(filename, "r") as file_in:
        file_contents = file_in.read()
        return file_contents


def save_file(filename, contents):
    with open(filename, "w") as file_out:
        file_out.write(contents)


def main():
    # example
    file = open_file("b64_or_b64_challenge.txt")
    print(base64_padding_decoder(file))
    output_list = encode("Lots of text that is needed for the base64 encoding. There will need to be long pieces for "
                         "this to work right.", "hi")
    for base64_word in output_list:
        print(base64_word)


if __name__ == "__main__":
    main()
