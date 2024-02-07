import abc

from spacecraft.communication.communicator import BaseCommunicator, MockCommunicator, IncorrectSecretCommunicator
from spacecraft.communication.encryption import VigenereCipher
from spacecraft.communication.state import ComsState, CommunicationState, BrainsState


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
    def dispatch(self, state: BrainsState) -> BaseCommunicator:
        return MockCommunicator()


class MockComsDispatcher(BaseCommunicationDispatcher):
    def __init__(self):
        self.__communicator = MockCommunicator()

    def dispatch(self, state: ComsState) -> BaseCommunicator:
        return self.__communicator


class DefaultComsDispatcher(BaseComsDispatcher):
    def __init__(self, secret: str):
        self.secret = secret

    def dispatch(self, state: ComsState) -> BaseCommunicator:
        if state.secret == self.secret:
            # secret is correct -> no need to encrypt
            return MockCommunicator()
        else:
            # secret is incorrect -> perform encryption/decryption
            return IncorrectSecretCommunicator(
                communicator=MockCommunicator(),
                encryption_secret=self.secret,  # actual secret
                decryption_secret=state.secret,  # incorrect secret
                encryption=VigenereCipher(),
            )
