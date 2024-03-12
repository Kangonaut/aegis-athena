<div align="center">
<img src="assets/mission-badge/mission-badge.png" alt="Aegis Athena mission badge" width="192"/>

# Aegis Athena: Project "Shielded Wisdom"

[![license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/Kangonaut/aegis-athena/blob/main/LICENSE)

</div>

## Welcome!

**Aegis Athena** is a little side-project for showcasing the capabilities of RAG. The user is thrown into an completely unknown environment (a spaceship) and is given the task of solving a unknown problem in that environment. An LLM powered RAG pipeline is supposed to aid the user in solving that problem by providing answers to the user's questions concerning this specific domain.

## Limitations

Although I achieved much better results, when using custom ReAct-like LLM agents, these pipelines require (only personal experience) very capable models (like GPT-4) to run satisfactorily. Thus, the main problem with this approach are the comparatively high operation costs.

This is why I used a simpler, less capable pipeline architecture.

## Retrieval Augmented Generation

![RAG pipeline](docs/rag-pipeline.png)

### Data Preparation

1. The documentation consists of multiple Markdown files. Firstly, these files are parsed using a custom Markdown reader (inherits the LlamaIndex `BaseReader` base class). This reader splits the documentation into `Nodes`, where each node represents a subsection with title and content. These **Block Chunks** represent the root nodes for the **Auto-Merging Retriever**.
1. In the next step, **Hierarchical Node Parsing** is used to split these root nodes into individual sentences using a custom sentence parser. The resulting **Sentence Chunks** reference their parent node, so that they can be merged and replaced by the **Auto-Merging Retriever**. The sentence boundaries are determined using the NLTK [`PunktSentenceTokenizer`](https://www.nltk.org/api/nltk.tokenize.PunktSentenceTokenizer.html).
1. The root nodes are stored in a **MongoDB** instance, since there is no need to perform similarity search on them. However, the leaf nodes are being retrieved using similarity search (actually hybrid search, which also utilizes similarity search), which is why there are stored in a **Weaviate** instance, alongside their vector embedding representation. This two-level setup, follows the approach of retrieving based on a smaller context, which intuitively makes retrieval more precise and adding surrounding context, in order to give the LLM more information. This principle is used in several advanced RAG methods, like Sentence-Window Retrieval or in this case: Auto-Merging Retrieval.

### Inference

1. In order to get that chat-bot behavior, the LlamaIndex `CondensePlusContextChatEngine` is used. Every time, the user sends a message, given the chat history, the chat engine condenses the interaction into a **Query**. This **Query** is then used as input for the retrieval system.
1. The first step of retrieval is to generate a hypothetical answer to the input query. This approach is called **HyDE** and it works under the assumption, that a hallucinated answer is often more similar to the actual answer document in the knowledge base, than the input query.
1. In the next step, both the **Query** and the **HyDE** document are combined to create a vector embedding, to be used for similarity search.
1. The combined document, as well as the vector embedding are then used to query the Weaviate instance and retrieve the top $k$ most similar documents. This step utilizes both **similarity search** (also called dense search), which is based on the distance between vector embeddings, and **BM25F keyword based search** (also called sparse search), which judges similarity based on matching keywords. This is thus called **Hybrid Search**.
1. As some of the retrieved nodes might be part of the same **Block Chunk**, the **Auto-Merging Retriever** groups them together and determines, if they should be replaced/merged by their parent node. This is controlled using the `simple_ratio_thresh` hyper-parameter, which determines the ratio of child nodes, that need to be retrieved, in order for them to be replaced by their parent node.
1. Although **Hybrid Search** already produces good results, they can be further improved using a **Cross-Encoder** based **Reranker**. The difference, between **Bi-Encoder** based retrieval (similarity search) and **Cross-Encoder** based retrieval is that, whereas the former approach creates vector embeddings for both the documents in the knowledge base as well as the input query and then computes similarity based on a distance metric (e.g.: cosine distance), the latter approach feeds both the input query and every potentially relevant document in the knowledge base into a classifier model, that outputs a relevance score between 0 and 1. Although this is computationally more expensive, we get a higher quality estimate of document relevance. This is why this step is preceeded by **Cross-Encoder** based retrieval, in order to narrow down the search space before using reranking to get the final context for the LLM.
1. Lastly, the **Chat History**, the retrieved **Context** and a **System Header** are combined to form the final prompt for the **LLM**, which then produces the response shown to the user. The system prompt, provides the LLM with some basic information about the situation and persona description for the chat-bot.

## Technologies

- [LlamaIndex](https://docs.llamaindex.ai/en/stable/): framework for implementing RAG pipelines and LLM Agents
- [Streamlit](https://docs.streamlit.io/): web app framework for AI/ML engineers and data scientist
- [Weaviate](https://weaviate.io/developers/weaviate): vector DB
- [Pydantic](https://docs.pydantic.dev/latest/): data validation library
- [TruLens](https://github.com/truera/trulens/): RAG evaluation framework
- [Arize Phoenix](https://docs.arize.com/phoenix/): AI observability framework
- [Ollama](https://ollama.com/): running LLM locally
- [MongoDB](https://www.mongodb.com/docs/): document DB

## Contributing

Feel free to fork the project, create a feature branch, and send me a pull request!

## License

This project is licensed under the [MIT License](https://github.com/Kangonaut/aegis-athena/blob/main/LICENSE).

## Contact

You can reach out to me through [Reddit](https://www.reddit.com/user/Kangonaut/). I'd love to chat about this project or any other interesting topics!

---

<div align="center">
<a href="https://www.buymeacoffee.com/kangonaut" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
</div>