import asyncio
import time  # NEW: For benchmarking
from fastapi import FastAPI
from pydantic import BaseModel
from similarity_sort_service import SimilaritySortService
from search_service import SearchService
from llm_service import LLMService

app = FastAPI()

search_service = SearchService()
sort_service = SimilaritySortService()
llm_service = LLMService()

class ChatBody(BaseModel):
    query: str

@app.get("/")
def welcome():
    return {"message": "Welcome to PulinSearchAI!!!"}

@app.post("/chat/normal")
async def normal_search(body: ChatBody):
    start_total = time.perf_counter()

    # 1. Scraping Phase
    t0 = time.perf_counter()
    search_results = await search_service.web_search(body.query)
    t1 = time.perf_counter()
    print(f"[LOG] Scraping Phase: {t1 - t0:.2f}s")

    # 2. Sorting Phase
    t0 = time.perf_counter()
    sorted_results = sort_service.sort_sources(body.query, search_results)
    t1 = time.perf_counter()
    print(f"[LOG] Sorting Phase: {t1 - t0:.2f}s")

    # 3. LLM Research (Qwen3)
    t0 = time.perf_counter()
    raw_facts = await llm_service.generate_response(body.query, sorted_results)
    t1 = time.perf_counter()
    print(f"[LOG] LLM Research (Local): {t1 - t0:.2f}s")

    # 4. LLM Synthesis (Groq)
    t0 = time.perf_counter()
    final_response = await llm_service.final_answer(raw_facts, body.query)
    t1 = time.perf_counter()
    print(f"[LOG] LLM Synthesis (Cloud): {t1 - t0:.2f}s")

    total_time = time.perf_counter() - start_total
    print(f"--- TOTAL TIME: {total_time:.2f}s ---\n")

    return {
        "mode": "normal", 
        "answer": final_response, 
        "sources": [{"id": i+1, "title": s["title"], "url": s["url"]} for i, s in enumerate(sorted_results)]
    }

@app.post("/chat/advanced")
async def hybrid_search(body: ChatBody):
    start_total = time.perf_counter()

    # 1. Scraping
    t0 = time.perf_counter()
    search_results = await search_service.web_search(body.query)
    t1 = time.perf_counter()
    print(f"[LOG] Scraping Phase: {t1 - t0:.2f}s")

    # 2. Hybrid Sorting
    t0 = time.perf_counter()
    hybrid_results = sort_service.hybrid_sort(body.query, search_results) 
    t1 = time.perf_counter()
    print(f"[LOG] Hybrid Sorting: {t1 - t0:.2f}s")

    # 3. LLM Research
    t0 = time.perf_counter()
    raw_facts = await llm_service.generate_response(body.query, hybrid_results)
    t1 = time.perf_counter()
    print(f"[LOG] LLM Research (Local): {t1 - t0:.2f}s")

    # 4. LLM Synthesis
    t0 = time.perf_counter()
    final_response = await llm_service.final_answer(raw_facts, body.query)
    t1 = time.perf_counter()
    print(f"[LOG] LLM Synthesis (Cloud): {t1 - t0:.2f}s")

    total_time = time.perf_counter() - start_total
    print(f"--- TOTAL TIME: {total_time:.2f}s ---\n")

    return {
        "mode": "hybrid", 
        "answer": final_response, 
        "sources": [{"id": i+1, "title": s["title"], "url": s["url"]} for i, s in enumerate(hybrid_results)]
    }