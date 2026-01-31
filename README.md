from typing import List
from semantic_router.encoders import HuggingFaceEncoder
from semantic_chunkers import StatisticalChunker
from sklearn.metrics.pairwise import cosine_similarity

class SimilaritySortService:
    def __init__(self):
        # 1. Setup the semantic encoder and chunker
        self.encoder = HuggingFaceEncoder(name="sentence-transformers/all-miniLM-L6-v2")
        self.chunker = StatisticalChunker(encoder=self.encoder)
        self.threshold = 0.3
        
    def sort_sources(self, query: str, search_results: List[dict]):
        all_semantic_chunks = []
        
        # Encode query once
        query_vector = self.encoder(["query: " + query])[0]

        for res in search_results:
            content = res.get('content')
            if not content: continue
            
            # Use the Statistical Chunker to get clean, thematic chunks
            # chunker() returns a list of lists, we take the first list [0]
            doc_chunks = self.chunker(docs=[content])[0]
            
            for chunk in doc_chunks:
                # Calculate similarity for the chunk
                # We access the text via chunk.content (or similar depending on version)
                chunk_text = chunk.content 
                chunk_vector = self.encoder([chunk_text])[0]
                
                # Reshape for sklearn similarity
                score = cosine_similarity([query_vector], [chunk_vector])[0][0]
                
                if score > self.threshold:
                    all_semantic_chunks.append({
                        "title": res.get("title"),
                        "url": res.get("url"),
                        "content": chunk_text,
                        "similarity_score": float(score)
                    })

        # Sort all chunks by similarity
        sorted_results = sorted(all_semantic_chunks, key=lambda x: x['similarity_score'], reverse=True)
        return sorted_results[:15] # Return top 15 chunks for the LLM