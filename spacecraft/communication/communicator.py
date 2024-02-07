import abc
import time
from typing import Iterator, Generator
import weaviate
from llama_index import VectorStoreIndex

from llama_index.llms import OpenAI
from llama_index.prompts import PromptTemplate, Prompt
from llama_index.query_pipeline import QueryPipeline
from llama_index.vector_stores import WeaviateVectorStore

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


class LlamaIndexCommunicator(BaseCommunicator):
    def __init__(self):
        self.llm = OpenAI(
            modeL="gpt-3.5-turbo",
            temperature=0.2,
        )

    def stream(self, message: str) -> Generator[MessageChunk, None, None]:
        prompt_template = PromptTemplate(
            "You are a helpful assistant"
            "Please answer the user query: {query}"
        )

        for chunk in self.llm.stream(prompt_template, query=message):
            time.sleep(0.1)
            yield MessageChunk(content=chunk)
