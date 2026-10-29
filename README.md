# AI Spec Chunker & RAG Pipeline Prep

A robust Python utility designed for parsing, structuring, and semantic chunking of massive technical specifications and engineering documentation. It extracts metadata (subsystem tags) and prepares text blocks for vector database ingestion in RAG (Retrieval-Augmented Generation) architectures.

## Key Features
- **Regex-Driven Sectioning:** Intelligently splits technical documents based on subsystem headers and brackets.
- **Sliding Window Chunking:** Breaks long requirements into manageable overlapping segments while preserving context.
- **Metadata Enrichment:** Tags every chunk with its respective subsystem for precise LLM retrieval.

## Tech Stack
- Python 3.x
- Built-in modules: `json`, `re`, `pprint`
