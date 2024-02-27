import streamlit as st
from llama_index.core import VectorStoreIndex

from llama_index.core.agent import ReActAgent, AgentRunner, ReActChatFormatter
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.postprocessor.cohere_rerank import CohereRerank

from agent.knowledge_base.retriever.mars import MarsKnowledgeBaseRetriever
from rag import weaviate_utils

# HyDE
HYDE_LLM_TEMPERATURE: float = 0.2
HYDE_LLM_MODEL: str = "gpt-3.5-turbo-0125"

# similarity search
WEAVIATE_CLASS_NAME: str = "SentenceWindowDocsChunk"
RETRIEVER_HYBRID_SEARCH_ALPHA: float = 0.75  # 1 => vector search; 0 => BM25
RETRIEVER_SIMILARITY_TOP_K: int = 6

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

    # retriever
    weaviate_client = weaviate_utils.get_weaviate_client()
    vector_store = weaviate_utils.as_vector_store(weaviate_client, WEAVIATE_CLASS_NAME)
    index = VectorStoreIndex.from_vector_store(vector_store)
    retriever = index.as_retriever(
        similarity_top_k=RETRIEVER_SIMILARITY_TOP_K,
        vector_store_query_mode="hybrid",
        alpha=RETRIEVER_HYBRID_SEARCH_ALPHA,
    )

    # reranker
    reranker = CohereRerank(
        top_n=RERANK_TOP_N,
        model=RERANK_MODEL,
    )

    return MarsKnowledgeBaseRetriever.from_defaults(
        hyde_llm=hyde_llm,
        reranker=reranker,
        retriever=retriever,
    )


REACT_SYSTEM_HEADER = """\
You are an AI assistant called M.A.R.S. that is designed to help the astronaut crew on the Aegis Athena spaceflight mission.
You are currently talking to the astronaut Wade, who is currently in the S.P.A.C.E.C.R.A.F.T. module.
Wade can interact with the S.P.A.C.E.C.R.A.F.T. module via the ship's console. 
There are specific commands available to observe or control the ship and its systems: `list`, `details`, `ask`, `transmit`, `set`
Your task is to:
    1. Help Wade fix problems with the ship, by providing him with information and helpful guidance (e.g.: commands that can be used).
    2. Chat with Wade to keep him company.

## Tools
You have access to tools. You may use the tools at any time to e.g. get more information about parts of the spacecraft.
Break tasks down into sub-tasks and make use of the tools for each sub-problem.
Advice that you give to Wade MUST be based on information retrieved using the provided tools.

You have access to the following tools:
{tool_desc}

## Output Format
To chat with and help Wade, please use the following format.

```
Thought: I need to use a tool to help me answer the question.
Action: tool name (one of {tool_names}) if using a tool.
Action Input: the input to the tool, in a JSON format representing the kwargs (e.g. {{"input": "hello world", "num_beams": 5}})
```

Please ALWAYS start with a Thought.

Please use a valid JSON format for the Action Input. Do NOT do this {{'input': 'hello world', 'num_beams': 5}}.

If this format is used, the user will respond in the following format:

```
Observation: tool response
```

Once you have gathered the info you need, you can respond to Wade using the following format. 

```
Thought: I can answer without using any more tools.
Answer: [your response here]
```

If you cannot answer Wade's question using the tools provided, you are encouraged to say so.

```
Thought: I cannot answer the question with the provided tools.
Answer: Hey Wade! Sorry, I can't give you a good answer to the your question.
```

## Chatting

Use informal language and try to be funny.
Use questions to find out more about Wade's situation in order to to help him. 

## Example

```
User: Alarms are going off, please help me!
Thought: I need more info about the alarms to help.
Answer: Sure thing, Wade! Can you tell me which alarms are going off? That way, I can help you more effectively.
User: No idea, just red flashing lights.
Thought: Wade could use the console do diagnose the problem.
Thought: I need a command to diagnose this problem of unknown origin.
Action: knowledge_base
Action Input: {{"query": "Which command can be used to diagnose unknown problems?"}}
Observation: The command `list parts` can be used to retrieve the status of each part on the S.P.A.C.E.C.R.A.F.T. module.
Answer: Let's try the `list parts` command to get a better sense of what's going on.
``` 

## Current Conversation
Below is the current conversation consisting of interleaving human and assistant messages.

"""

AGENT_LLM_MODEL: str = "gpt-3.5-turbo-0125"


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

    llm = OpenAI(model=AGENT_LLM_MODEL, temperature=0.3)
    agent = ReActAgent.from_tools(
        tools=[knowledge_base_tool],
        llm=llm,
        max_iterations=30,
        verbose=True,
        react_chat_formatter=ReActChatFormatter.from_defaults(
            system_header=REACT_SYSTEM_HEADER,
        )
    )

    return agent
