import abc
import time
from typing import Iterator, Generator

from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core.query_engine import BaseQueryEngine
from llama_index.core.agent import AgentRunner

from spacecraft.communication.encryption import BaseEncryption
from spacecraft.communication.message import MessageChunk


class BaseCommunicator(abc.ABC):
    @abc.abstractmethod
    def stream(self, message: str) -> Generator[MessageChunk, None, None]:
        pass


class MockCommunicator(BaseCommunicator):
    """
    This communicator always answers with a dummy message.

    **NOTE: Should only be used for testing!**
    """

    __MOCK_MESSAGE = "How is the weather today? I hope it's good. Anyway, everything's fine down here. Hope to hear from you soon! Bye!"
    __DURATION_PER_WORD: float = 0.1

    def stream(self, message: str) -> Generator[MessageChunk, None, None]:
        tokens = self.__MOCK_MESSAGE.split(" ")
        for token in tokens:
            time.sleep(self.__DURATION_PER_WORD)  # simulate response time
            yield MessageChunk(content=f"{token} ")


class EncryptedCommunicator(BaseCommunicator):
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

    def stream(self, message: str) -> Generator[MessageChunk, None, None]:
        plaintext_stream = self.__communicator.stream(message)

        if self.__encryption_secret == self.__decryption_secret:
            return plaintext_stream

        encrypted_stream = self.__encryption.encrypt(
            input_stream=plaintext_stream,
            secret=self.__encryption_secret,
        )
        decrypted_stream = self.__encryption.decrypt(
            input_stream=encrypted_stream,
            secret=self.__decryption_secret,
        )
        return decrypted_stream


class LlamaIndexQueryEngineCommunicator(BaseCommunicator):
    def __init__(self, query_engine: BaseQueryEngine):
        self.query_engine = query_engine

    def stream(self, message: str) -> Generator[MessageChunk, None, None]:
        for chunk in self.query_engine.query(message).response_gen:
            yield MessageChunk(chunk)


class LlamaIndexChatEngineCommunicator(BaseCommunicator):
    def __init__(self, chat_engine: BaseChatEngine):
        self.chat_engine = chat_engine

    def stream(self, message: str) -> Generator[MessageChunk, None, None]:
        # response to indicate to the user that the request is being handled
        yield MessageChunk("thinking ...\n")

        response = self.chat_engine.chat(message)
        yield MessageChunk(response.response)


class LlamaIndexAgentCommunicator(BaseCommunicator):
    def __init__(self, agent_runner: AgentRunner):
        self.agent_runner = agent_runner

    def stream(self, message: str) -> Generator[MessageChunk, None, None]:
        # NOTE: stream_chat is faulty
        # for chunk in self.agent_runner.stream_chat(message).response_gen:
        #     yield MessageChunk(chunk)

        response = self.agent_runner.chat(message)
        yield MessageChunk(content=response.response)
