from base64 import b64encode
from typing import TextIO

base64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
dict = [x for x in base64_alphabet]
padding_bits = ""


def get_message(padding_bits: str) -> str:
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
    equal_sign_index = word.index('=')
    char_to_modify = word[equal_sign_index - 1]
    shift_amount = int(secret, 2)
    encoded_char = dict[dict.index(char_to_modify) + shift_amount]
    encoded_word = word[:equal_sign_index - 1] + encoded_char + '=' * (len(word) - equal_sign_index)
    return encoded_word


def encode(text, secret):
    words = text.split(' ')
    base64_words = [b64encode((word + " ").encode('ascii')).decode('ascii') for word in words]
    max_secret_length = 2 * sum(word.count('=') for word in base64_words)
    if 7 * len(secret) + 16 > max_secret_length:
        raise ValueError('*!* Need more text to encode this secret.')

    bin_secret = bin(len(secret))[2:].zfill(16)
    for char in secret:
        bin_secret += bin(ord(char))[2:].zfill(7)
    bin_secret += (max_secret_length - len(bin_secret)) * '0'

    encoded_list = []
    for word in base64_words:
        equals_count = word.count('=')
        if equals_count > 0:
            encoded_list.append(encode_word(word, bin_secret[:2 * equals_count]))
            bin_secret = bin_secret[2 * equals_count:]  # Move to the next section of the secret
        else:
            encoded_list.append(word)  # If no '=' in the word, leave it as is

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
