import abc

from spacecraft.communication.communicator import BaseCommunicator, MockCommunicator, IncorrectSecretCommunicator
from spacecraft.communication.encryption import VigenereCipher
from spacecraft.communication.state import CommunicationState


class BaseCommunicationDispatcher(abc.ABC):
    """
    The dispatcher decides which communicator (:code:`BaseCommunicator`) should handle the communication request.
    """

    @abc.abstractmethod
    def dispatch(self, state: CommunicationState) -> BaseCommunicator:
        pass


class MockCommunicationDispatcher(BaseCommunicationDispatcher):
    """
    This dispatcher always chooses the :code:`MockCommunicator`.

    **NOTE: Should only be used for testing!**
    """

    def __init__(self):
        self.__communicator = MockCommunicator()

    def dispatch(self, state: CommunicationState) -> BaseCommunicator:
        return self.__communicator


class DefaultCommunicationDispatcher(BaseCommunicationDispatcher):
    def __init__(self, secret: str):
        self.secret = secret

    def dispatch(self, state: CommunicationState) -> BaseCommunicator:
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
