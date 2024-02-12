# M.A.R.S. RAG Diary

## M.A.R.S. v1.0

This version utilizes a basic RAG setup, consisting of a Weaviate vector database and the `gpt-3.5-turbo` model for synthesis.
The `MarkdownDocsChunk` Weaviate class is used, which has chunks produced using the `MarkdownNodeParser`.
The `simple-eval-questions` dataset was used in combination with `gpt-4` for the evaluation process.

### Results

- Groundedness: 0.77
- Answer Relevance: 0.82
- Context Relevance: 0.58

## M.A.R.S. v1.1

The same architecture as v1.0, but utilizing the `gpt-4` model for synthesis.

### Results

- Groundedness: 0.68
- Answer Relevance: 0.57
- Context Relevance: 0.9