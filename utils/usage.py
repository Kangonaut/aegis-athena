import os
import streamlit as st

from . import mongodb
from usage.openai.observer import OpenAIUsageObserver
from usage.mongodb.usage_store import MongoDBUsageStore


def init_usage_tracking() -> None:
    store = MongoDBUsageStore(
        mongodb_client=mongodb.get_client()
    )
    observer = OpenAIUsageObserver(store)
