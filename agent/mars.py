import streamlit as st
from llama_index.core import VectorStoreIndex, StorageContext

from llama_index.core.agent import ReActAgent, AgentRunner, ReActChatFormatter
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.postprocessor.cohere_rerank import CohereRerank

from agent.knowledge_base.retriever.mars import MarsKnowledgeBaseRetriever
from rag import weaviate_utils, mongodb_utils

# HyDE
HYDE_LLM_TEMPERATURE: float = 0.2
HYDE_LLM_MODEL: str = "gpt-3.5-turbo-0125"

# similarity search
WEAVIATE_CLASS_NAME: str = "AutoMergingDocsChunk"
RETRIEVER_HYBRID_SEARCH_ALPHA: float = 0.85  # 1 => vector search; 0 => BM25
RETRIEVER_SIMILARITY_TOP_K: int = 15

# auto-merging retrieval
AUTO_MERGING_RATION_THRESHOLD: float = 0.2

# reranking
RERANK_TOP_N: int = 3
RERANK_MODEL: str = "rerank-english-v2.0"


@st.cache_resource
def get_knowledge_base_retriever():
    # HyDE
    hyde_llm = OpenAI(
        model=HYDE_LLM_MODEL,
        temperature=HYDE_LLM_TEMPERATURE,
    )

    # Weaviate
    weaviate_client = weaviate_utils.get_weaviate_client()
    weaviate_vector_store = weaviate_utils.as_vector_store(weaviate_client, WEAVIATE_CLASS_NAME)
    weaviate_index = VectorStoreIndex.from_vector_store(weaviate_vector_store)
    weaviate_retriever = weaviate_index.as_retriever(
        similarity_top_k=RETRIEVER_SIMILARITY_TOP_K,
        vector_store_query_mode="hybrid",
        alpha=RETRIEVER_HYBRID_SEARCH_ALPHA,
    )

    # MongoDB
    mongodb_client = mongodb_utils.get_client()
    mongodb_docstore = mongodb_utils.as_docstore(mongodb_client)
    mongodb_storage_context = StorageContext.from_defaults(docstore=mongodb_docstore)

    # auto-merging retriever
    auto_merging_retriever = AutoMergingRetriever(
        simple_ratio_thresh=AUTO_MERGING_RATION_THRESHOLD,
        vector_retriever=weaviate_retriever,
        storage_context=mongodb_storage_context,
        verbose=True,
    )

    # reranker
    reranker = CohereRerank(
        top_n=RERANK_TOP_N,
        model=RERANK_MODEL,
    )

    return MarsKnowledgeBaseRetriever.from_defaults(
        hyde_llm=hyde_llm,
        reranker=reranker,
        retriever=auto_merging_retriever,
    )


REACT_SYSTEM_HEADER = """\
You are an AI assistant called MARS that is designed to help the astronaut crew on the Aegis Athena spaceflight mission.
You are currently talking to the astronaut Wade, who is currently in the SPACECRAFT module.
Wade can only interact with the SPACECRAFT module via the ship's console.

Always start by formulating a query for retrieving relevant information from the knowledge base. This is a `Thought`. Do NOT do this: `Thought: (Implicit) I can answer without any more tools!`
Then select the knowledge_base (`Action`) and provide your query as input (`Action Input`).
Please use a valid JSON format for the Action Input. Do NOT do this {{'query': 'What commands are available?'}}.
Finally, answer the user's query using the context provided by the knowledge_base
Answer the user's query ONLY using context provided by the knowledge base and not prior knowledge.

## Example

### Conversation

User: What commands can be used to get an overview of the ship's status?
Assistant: You can use the `list` command to list all systems (using `list systems`), along with their status info. 
User: Are there other things that can be listed using this command?

### Output

Thought: How do you use the `list` command? 
Action: knowledge_base
Action Input: {{"query": "How do you use the `list` command?"}}
Observation: You can use the `list` command in one of two ways. Using `list systems`, which will list all systems along with status info or using `list systems`, which will list all parts, along with their corresponding part ID and status info.
Answer: Yes, you can also use `list parts` to list all parts, along with their corresponding part ID and status info.

## Current Conversation
Below is the current conversation consisting of interleaving human and assistant messages.

"""

AGENT_LLM_MODEL: str = "gpt-3.5-turbo-0125"
# AGENT_LLM_MODEL: str = "gpt-3.5-turbo-0613"
# AGENT_LLM_MODEL: str = "gpt-4-0125-preview"

AGENT_LLM_TEMPERATURE: float = 0.1

def build_agent() -> AgentRunner:
    knowledge_base_retriever = get_knowledge_base_retriever()
    knowledge_base_tool = FunctionTool.from_defaults(
        fn=knowledge_base_retriever.retrieve_formatted,
        name="knowledge_base",
        description="Provides information about the Aegis Athena spaceflight mission, "
                    "the S.P.A.C.E.C.R.A.F.T. (command/service) module "
                    "and the A.P.O.L.L.O. (lunar lander) module. "
                    "Can be used to gather information about systems or parts."
                    "Use a question as input to the tool."
    )

    llm = OpenAI(model=AGENT_LLM_MODEL, temperature=AGENT_LLM_TEMPERATURE)
    agent = ReActAgent.from_tools(
        tools=[knowledge_base_tool],
        llm=llm,
        max_iterations=10,
        verbose=True,
        react_chat_formatter=ReActChatFormatter.from_defaults(
            system_header=REACT_SYSTEM_HEADER,
        )
    )

    return agent
