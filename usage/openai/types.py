from typing import ClassVar

from usage.base.types import BaseUsageEntry


class OpenAIUsageEntry(BaseUsageEntry):
    service_id: ClassVar[str] = "openai"
