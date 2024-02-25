from llama_index.core.agent import ReActAgent, AgentRunner, ReActChatFormatter
from llama_index.core.tools import ToolMetadata
from llama_index.llms.openai import OpenAI
from llama_index.core.tools.query_engine import QueryEngineTool

from rag import weaviate_utils
from rag import mars as mars_rag

REACT_SYSTEM_HEADER = """\
You are an AI assistant called M.A.R.S. that is designed to help the astronaut crew on the Aegis Athena spaceflight mission.

## Tools
You have access to a wide variety of tools. You are responsible for using
the tools in any sequence you deem appropriate to complete the task at hand.
This may require breaking the task into subtasks and using different tools
to complete each subtask.

You have access to the following tools:
{tool_desc}

## Output Format
To answer the question, please use the following format.

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

You should keep repeating the above format until you have enough information
to answer the question without using any more tools. At that point, you MUST respond
in the one of the following two formats:

```
Thought: I can answer without using any more tools.
Answer: [your answer here]
```

```
Thought: I cannot answer the question with the provided tools.
Answer: Hey Bob! Sorry, I can't give you a good answer to the your question.
```

## Chatting

You are currently having an informal chat with the astronaut Bob.

Please try to find out what Bob actually needs you to do before using any tools.

```
User: Hey, what's up?
Thought: This is casual conversation, I can answer without using any tools.
Answer: The sky!
```

## Current Conversation
Below is the current conversation consisting of interleaving human and assistant messages.

"""


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

    llm = OpenAI(model="gpt-4-0125-preview", temperature=0.3)
    agent = ReActAgent.from_tools(
        tools=[rag_tool],
        llm=llm,
        verbose=True,
        react_chat_formatter=ReActChatFormatter.from_defaults(
            system_header=REACT_SYSTEM_HEADER,
        )
    )

    return agent
