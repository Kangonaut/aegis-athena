import abc
import time
from typing import Iterator

from spacecraft.communication.encryption import BaseEncryption
from spacecraft.communication.message import MessageChunk


class BaseCommunicator(abc.ABC):
    @abc.abstractmethod
    def stream(self, message: str) -> Iterator[MessageChunk]:
        pass


class MockCommunicator(BaseCommunicator):
    """
    This communicator always answers with a dummy message.

    **NOTE: Should only be used for testing!**
    """

    __MOCK_MESSAGE = "How is the weather today? I hope it's good. Anyway, everything's fine down here. Hope to hear from you soon! Bye!"
    __DURATION_PER_CHAR: float = 0.1

    def stream(self, message: str) -> Iterator[MessageChunk]:
        tokens = self.__MOCK_MESSAGE.split(" ")
        for token in tokens:
            time.sleep(self.__DURATION_PER_CHAR)  # simulate response time
            yield MessageChunk(content=token)


class IncorrectSecretCommunicator(BaseCommunicator):
    """
    This should be used as a wrapper around the real communicator, in the scenario that the configured secret is not correct.
    In that case, the response is first encrypted using the correct secret and then decrypted using the configured secret.
    """

    def __init__(
            self,
            communicator: BaseCommunicator,
            encryption_secret: str,
            decryption_secret: str,
            encryption: BaseEncryption
    ):
        self.__communicator = communicator
        self.__encryption_secret = encryption_secret
        self.__decryption_secret = decryption_secret
        self.__encryption = encryption

    def stream(self, message: str) -> Iterator[MessageChunk]:
        plaintext_stream = self.__communicator.stream(message)
        encrypted_stream = self.__encryption.encrypt(
            input_stream=plaintext_stream,
            secret=self.__encryption_secret,
        )
        decrypted_stream = self.__encryption.decrypt(
            input_stream=encrypted_stream,
            secret=self.__decryption_secret,
        )
        return decrypted_stream
