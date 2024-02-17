# M.A.R.S. RAG Diary

## M.A.R.S. v1.0

This version utilizes a basic RAG setup, consisting of a Weaviate vector database and the `gpt-3.5-turbo` model for synthesis.
The `MarkdownDocsChunk` Weaviate class is used, which has chunks produced using the `MarkdownNodeParser`.
The `simple-eval-questions` dataset was used in combination with `gpt-4` for the evaluation process.

### Results

- Groundedness: 0.77
- Answer Relevance: 0.82
- Context Relevance: 0.58

### Thoughts

There are a few questions that have an answer relevance and groundedness score of both 1, but score poorly on context relevance, due to the fact that although the answer is provided in one of the retrieved nodes, it also retrieves nodes which are less important to the query.
This might be solved by using a reranker.

## M.A.R.S. v1.1

The same architecture as v1.0, but utilizing the `gpt-4` model for synthesis.

### Results

- Groundedness: 0.68
- Answer Relevance: 0.57
- Context Relevance: 0.9

### Thoughts

Using a more advanced model, does not seem to drastically increase the overall performance of this basic RAG pipline.

## M.A.R.S. v1.2

The same architecture as v1.0, but before the retrieved nodes are passed as context to the LLM, they are reranked using the `SentenceTransformerRerank` module and the `BAAI/bge-reranker-base` transformer model from FlagEmbedding.

### Results

- Groundedness: 0.86
- Answer Relevance: 0.82
- Context Relevance: 0.68

### Thoughts

As can be seen, the approach improved the context relevance metric, which also causes the groundedness metric to go up. This makes sense, since a more relevant context makes it easier to form an answer that is backed up by mentioned context.

## M.A.R.S. v2.0

This version uses sentence window retrieval, in order to give the synthesizer more context and make the retrieval step more precise.
The Weaviate class `SentenceWindowDocsChunk` is used as a datasource. A parameter of `window_size = 3` is used for the data loading stage.
Furthermore, v2.0 also utilizes a re-ranker stage also using the `BAAI/bge-reranker-base` model. 

### Results

- Groundedness: 0.82
- Answer Relevance: 0.75
- Context Relevance: 0.77

### Thoughts

This approach seems to have improved the context relevance metric, which proves the intuition behind the approach and also shows that this approach is also feasible for this dataset.

Regarding the decrease of answer relevance, after looking through the samples that scored badly, I did not agree with the LLMs evaluation, since they all answered the query fairly well. Thus, I don't think this really has an effect on answer relevance.

## M.A.R.S. v3.0

The architecture is based on v2.0, but adds the HyDE query transformation method before the retrieval step.
HyDE (Hypothetical Document Embedding) generates a hypothetical answer to the user query first, which is then used as the query string in the retrieval step.
In this case, not only the HyDE query, but also the original query is used for retrieval (`include_original=True`).

Default HyDE prompt:

```python
HYDE_TMPL = (
    "Please write a passage to answer the question\n"
    "Try to include as many key details as possible.\n"
    "\n"
    "\n"
    "{context_str}\n"
    "\n"
    "\n"
    'Passage:"""\n'
)
```

### Results

- Groundedness: 0.82
- Answer Relevance: 0.86
- Context Relevance: 0.77

### Thoughts

Compared to v2.0, groundedness and context relevance did not improve nor deteriorate. Answer relevance was only slightly improved.
However, since HyDE should mainly affect context relevance, the improvement in answer relevance is probably not a sign of an improvement in the architecture, but merely random noise that comes with the sometimes inconsistent evaluation of the feedback LLM.
Looking at some actual examples that were had a better answer relevance score, this seems to be true. This is a drawback of the rather small dataset size of just 20 questions. However, since running evals with GPT-4 as a feedback LLM is pretty expensive, I presently cannot afford to use a larger evaluation dataset.

## M.A.R.S. v4.0

This version of M.A.R.S. is used to try out how well the pipeline performs using smaller models. 
The architecture is the same as v3.0, except from the LLM used, which is the Llama-2-7b-chat-hf (`llama2:7b`) model. The model is being run locally on an Ollama server instance.

### Results

- Groundedness: 0.86
- Answer Relevance: 0.88
- Context Relevance: 0.78

### Thoughts

As can be seen, the smaller LLama2-7b model still performs great, even slightly better than GPT-3.5-turbo, although that might be random error in judging.
However, executing a single query pipeline pass almost took 4 minutes on my local machine. Since this is not acceptable, I will repeat this experiment with even smaller models.

## M.A.R.S. v4.1

This version of M.A.R.S. is used to try out how well the pipeline performs using smaller models. 
The architecture is the same as v3.0, except from the LLM used, which is the Llama-2-7b-chat-hf (`llama2:7b`) model. The model is being run locally on an Ollama server instance.

### Results

- Groundedness: 0.86
- Answer Relevance: 0.88
- Context Relevance: 0.78
