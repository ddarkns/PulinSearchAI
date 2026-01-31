import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from similarity_sort_service import SimilaritySortService
from search_service import SearchService
from llm_service import LLMService

app = FastAPI()

# Global service instances
search_service = SearchService()
sort_service = SimilaritySortService()
llm_service = LLMService()

class ChatBody(BaseModel):
    query: str

@app.get("/")
def welcome():
    return {"message": "Welcome to PulinSearchAI!!!"}

@app.post("/chat/normal")
def normal_search(body: ChatBody):
    # 1. Fetch web results ASYNCHRONOUSLY (Huge speed boost)
    search_results = search_service.web_search(body.query)
    
    # 2. Sort using Semantic logic
    sorted_results = sort_service.sort_sources(body.query, search_results)
    
    # 3. Two-Stage LLM Relay (Lighter model for research)
    raw_facts = llm_service.generate_response(body.query, sorted_results)
    final_response = llm_service.final_answer(raw_facts, body.query)
    
    return {
        "mode": "normal", 
        "answer": final_response, 
        "sources": [{"id": i+1, "title": s["title"], "url": s["url"], "content":s["content"]} for i, s in enumerate(sorted_results)]
    }

@app.post("/chat/advanced")
def hybrid_search(body: ChatBody):
    # 1. Fetch web results ASYNCHRONOUSLY
    search_results = search_service.web_search_async(body.query)
    
    # 2. Sort using Hybrid logic
    hybrid_results = sort_service.hybrid_sort(body.query, search_results) 
    
    # 3. Two-Stage LLM Relay
    raw_facts = llm_service.generate_response_async(body.query, hybrid_results)
    final_response = llm_service.final_answer_async(raw_facts, body.query)
    
    return {
        "mode": "hybrid", 
        "answer": final_response, 
        "sources": [{"id": i+1, "title": s["title"], "url": s["url"]} for i, s in enumerate(hybrid_results)]
    }