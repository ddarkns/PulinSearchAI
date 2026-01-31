from typing import List
import numpy as np
from semantic_router.encoders import HuggingFaceEncoder
from semantic_chunkers import StatisticalChunker
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi

class SimilaritySortService:
    def __init__(self):
        # 1. Setup the semantic encoder (all-miniLM)
        # Using the capital 'F' version as we found earlier
        try:
            from semantic_router.encoders import HuggingFaceEncoder
        except ImportError:
            from semantic_router.encoders import HuggingfaceEncoder
            
        self.encoder = HuggingFaceEncoder(name="sentence-transformers/all-miniLM-L6-v2")
        
        # 2. Setup the Statistical Chunker
        self.chunker = StatisticalChunker(encoder=self.encoder)
        
        # 3. Tuning parameters
        self.semantic_threshold = 0.3
        self.hybrid_threshold = 0.25  # Lower threshold for hybrid to allow keyword boosts

    def _get_bm25_scores(self, query: str, chunk_texts: List[str]) -> np.ndarray:
        """Calculates BM25 keyword relevance scores for a list of chunks."""
        if not chunk_texts:
            return np.array([])
            
        tokenized_query = query.lower().split()
        tokenized_corpus = [doc.lower().split() for doc in chunk_texts]
        
        bm25 = BM25Okapi(tokenized_corpus)
        scores = bm25.get_scores(tokenized_query)
        
        # Normalize scores to a 0-1 range roughly (BM25 can be > 1)
        if len(scores) > 0 and np.max(scores) > 0:
            return scores / np.max(scores)
        return scores

    def _extract_all_chunks(self, search_results: List[dict]) -> List[dict]:
        """Helper to process raw search results into a flat list of semantic chunks."""
        all_chunks = []
        for res in search_results:
            content = res.get('content')
            if not content:
                continue
            
            # Use Statistical Chunker to find thematic boundaries
            doc_chunks = self.chunker(docs=[content])[0]
            
            for chunk in doc_chunks:
                all_chunks.append({
                    "title": res.get("title"),
                    "url": res.get("url"),
                    "content": chunk.content
                })
        return all_chunks

    def sort_sources(self, query: str, search_results: List[dict]):
        """
        NORMAL SEARCH: Standard Semantic-only sorting.
        Best for: Understanding meaning and intent.
        """
        chunks = self._extract_all_chunks(search_results)
        if not chunks:
            return []

        query_vector = self.encoder(["query: " + query])[0]
        chunk_texts = [c["content"] for c in chunks]
        chunk_vectors = self.encoder(chunk_texts)
        
        # Calculate Cosine Similarity
        semantic_scores = cosine_similarity([query_vector], chunk_vectors)[0]

        sorted_results = []
        for i, chunk in enumerate(chunks):
            score = float(semantic_scores[i])
            if score > self.semantic_threshold:
                chunk["similarity_score"] = score
                sorted_results.append(chunk)

        # Sort by score descending
        sorted_results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return sorted_results[:15]

    def hybrid_sort(self, query: str, search_results: List[dict]):
        """
        HYBRID SEARCH: Combines Semantic (70%) and Keyword (30%) scores.
        Best for: Exact matches, technical terms, and serial numbers.
        """
        chunks = self._extract_all_chunks(search_results)
        if not chunks:
            return []

        chunk_texts = [c["content"] for c in chunks]

        # 1. Get Semantic Scores (Vectors)
        query_vector = self.encoder(["query: " + query])[0]
        chunk_vectors = self.encoder(chunk_texts)
        semantic_scores = cosine_similarity([query_vector], chunk_vectors)[0]

        # 2. Get Keyword Scores (BM25)
        keyword_scores = self._get_bm25_scores(query, chunk_texts)

        # 3. Combine scores
        final_results = []
        for i, chunk in enumerate(chunks):
            # Weighted average: 70% Meaning, 30% Exact Keywords
            combined_score = (semantic_scores[i] * 0.7) + (keyword_scores[i] * 0.3)
            
            if combined_score > self.hybrid_threshold:
                chunk["similarity_score"] = float(combined_score)
                final_results.append(chunk)

        # 4. Final Sort
        final_results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return final_results[:15]