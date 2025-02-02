import abc
from typing import Iterator, Generator, Self, Type, Callable

from spacecraft.communication.message import MessageChunk


def is_letter(char: str) -> bool:
    char = char.upper()
    return "A" <= char <= "Z"


def caesar_cipher(letter: str, offset: int) -> str:
    is_upper: bool = letter.isupper()
    letter = letter.upper()

    letter_code: int = ord(letter) - ord("A")
    encrypted_letter_code: int = (letter_code + offset) % 26
    encrypted_char: str = chr(encrypted_letter_code + ord("A"))

    return encrypted_char if is_upper else encrypted_char.lower()


def infinite_secret(secret: str) -> Generator[str, None, None]:
    idx: int = 0
    while True:
        yield secret[idx % len(secret)]
        idx += 1


class BaseEncryption(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def encrypt(cls, input_stream: Iterator[MessageChunk], secret: str) -> Generator[MessageChunk, None, None]:
        pass

    @classmethod
    @abc.abstractmethod
    def decrypt(cls, input_stream: Iterator[MessageChunk], secret: str) -> Generator[MessageChunk, None, None]:
        pass


class VigenereCipher(BaseEncryption):
    @staticmethod
    def __handle_input_stream(
            input_stream: Iterator[MessageChunk],
            secret: str,
            transform: Callable[[str, Generator[str, None, None]], str]
    ) -> Generator[MessageChunk, None, None]:
        secret_generator = infinite_secret(secret)

        for token in input_stream:
            transformed_token: str = ""

            for char in token.content:
                if is_letter(char):
                    transformed_token += transform(char, secret_generator)
                else:
                    transformed_token += char

            yield MessageChunk(content=transformed_token)

    @staticmethod
    def __encrypt_char(char: str, secret_generator: Generator[str, None, None]) -> str:
        secret_char = next(secret_generator)
        secret_char = secret_char.upper()
        offset: int = ord(secret_char) - ord("A")
        return caesar_cipher(char, offset)

    @staticmethod
    def __decrypt_char(char: str, secret_generator: Generator[str, None, None]) -> str:
        secret_char = next(secret_generator)
        secret_char = secret_char.upper()
        offset: int = ord(secret_char) - ord("A")
        offset *= -1
        return caesar_cipher(char, offset)

    @classmethod
    def encrypt(cls, input_stream: Iterator[MessageChunk], secret: str) -> Generator[MessageChunk, None, None]:
        return cls.__handle_input_stream(
            input_stream,
            secret,
            cls.__encrypt_char,
        )

    @classmethod
    def decrypt(cls, input_stream: Iterator[MessageChunk], secret: str) -> Generator[MessageChunk, None, None]:
        return cls.__handle_input_stream(
            input_stream,
            secret,
            cls.__decrypt_char,
        )
