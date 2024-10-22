import abc

from spacecraft.communication.communicator import BaseCommunicator, MockCommunicator, EncryptedCommunicator, \
    LlamaIndexQueryEngineCommunicator, LlamaIndexAgentCommunicator, LlamaIndexChatEngineCommunicator
from spacecraft.communication.encryption import VigenereCipher
from spacecraft.communication.state import ComsState, CommunicationState, BrainsState

from agent import mars as mars_agent
from chat_engine import mars as mars_chat_engine


class BaseCommunicationDispatcher(abc.ABC):
    @abc.abstractmethod
    def dispatch(self, state: CommunicationState) -> BaseCommunicator:
        pass


class BaseComsDispatcher(BaseCommunicationDispatcher):
    @abc.abstractmethod
    def dispatch(self, state: ComsState) -> BaseCommunicator:
        pass


class BaseBrainsDispatcher(BaseCommunicationDispatcher):
    @abc.abstractmethod
    def dispatch(self, state: BrainsState) -> BaseCommunicator:
        pass


class DefaultBrainsDispatcher(BaseBrainsDispatcher):
    def __init__(self):
        # self._communicator = LlamaIndexAgentCommunicator(agent_runner=mars_agent.build_agent())
        self._communicator = LlamaIndexChatEngineCommunicator(chat_engine=mars_chat_engine.build_chat_engine())

    def dispatch(self, state: BrainsState) -> BaseCommunicator:
        return self._communicator


class MockComsDispatcher(BaseCommunicationDispatcher):
    def __init__(self):
        self.__communicator = MockCommunicator()

    def dispatch(self, state: ComsState) -> BaseCommunicator:
        return self.__communicator


class DefaultComsDispatcher(BaseComsDispatcher):
    def __init__(self, secret: str):
        self.secret = secret

    def dispatch(self, state: ComsState) -> BaseCommunicator:
        return EncryptedCommunicator(
            communicator=MockCommunicator(),
            encryption_secret=self.secret,  # actual secret
            decryption_secret=state.secret,  # incorrect secret
            encryption=VigenereCipher(),
        )
