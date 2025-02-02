from typing import Callable

from openai.resources.completions import Completions
from openai.resources.chat.completions import Completions as ChatCompletions

from usage.base.observer import BaseUsageObserver
from usage.base.types import UsageEntry
from usage.base.usage_store import BaseUsageStore
from usage.openai.types import SERVICE_NAME


class OpenAIUsageObserver(BaseUsageObserver):
    def __init__(
            self,
            store: BaseUsageStore,
    ):
        super().__init__(store)

        # add proxy for completion
        completion_wrapper = self.__usage_decorator(fn=Completions.create)
        Completions.create = completion_wrapper

        # add proxy for chat completion
        chat_completion_wrapper = self.__usage_decorator(fn=ChatCompletions.create)
        ChatCompletions.create = chat_completion_wrapper

    def __usage_decorator(self, fn: Callable) -> Callable:
        def wrapper(resource_self, *args, **kwargs) -> any:
            # call original function
            result = fn(resource_self, *args, **kwargs)

            # extract properties
            model = result.model
            num_input_tokens = result.usage.prompt_tokens
            num_output_tokens = result.usage.completion_tokens

            # store entry
            self._store.add_entry(
                entry=UsageEntry(
                    model=model,
                    num_input_tokens=num_input_tokens,
                    num_output_tokens=num_output_tokens,
                    service=SERVICE_NAME,
                )
            )

            # return function result
            return result

        return wrapper
