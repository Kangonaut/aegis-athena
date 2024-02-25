import llama_index.core


def init_observation():
    llama_index.core.set_global_handler("arize_phoenix")
