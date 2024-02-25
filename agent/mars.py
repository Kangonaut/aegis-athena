from llama_index.core.agent import ReActAgent, AgentRunner
from llama_index.core.tools import ToolMetadata
from llama_index.llms.openai import OpenAI
from llama_index.core.tools.query_engine import QueryEngineTool

from rag import weaviate_utils
from rag import mars as mars_rag


def build_agent() -> AgentRunner:
    rag_query_engine = mars_rag.get_v5_2()

    rag_tool = QueryEngineTool(
        query_engine=rag_query_engine,
        metadata=ToolMetadata(
            name="knowledge_base_retriever",
            description="Provides information about the Aegis Athena spaceflight mission, "
                        "the S.P.A.C.E.C.R.A.F.T. (command/service) module "
                        "and the A.P.O.L.L.O. (lunar lander) module."
                        "Use a detailed plain text question as input to the tool.",
        ),
    )

    llm = OpenAI(model="gpt-3.5-turbo")
    agent = ReActAgent.from_tools(
        tools=[rag_tool],
        llm=llm,
        verbose=True,
    )

    return agent
