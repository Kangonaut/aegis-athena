import os
import streamlit as st

from . import mongodb
from usage.openai.observer import OpenAIUsageObserver
from usage.mongodb.usage_store import MongoDBUsageStore


def get_usage_store() -> MongoDBUsageStore:
    store = MongoDBUsageStore(
        mongodb_client=mongodb.get_client()
    )
    return store


def init_usage_tracking() -> None:
    store = get_usage_store()
    observer = OpenAIUsageObserver(store)
