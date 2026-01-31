import os
from typing import List
from langchain_ollama import ChatOllama  # NEW: For local Qwen3
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import Settings

settings = Settings()

class LLMService:
    def __init__(self):
        # STAGE 1: The Local "Deep Brain" (Ollama)
        # We use Qwen3 locally. Make sure you've run `ollama pull qwen3`
        self.research_llm = ChatOllama(
             model="qwen3:8b", 
             temperature=0.1,
    # CRITICAL: Increase context from default 4096 to 32768
           num_ctx=32768, 
    # Optional: ensure it uses your 8GB VRAM
          num_gpu=35 
       )

        # STAGE 2: The "Fast Tongue" (Groq)
        # Keeping Llama 3.3 70B for its insane speed and polish.
        self.synthesis_llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.environ.get("GROQ_API_KEY"),
            temperature=0.2
        )

    def generate_response(self, query: str, search_results: List[dict]):
        # [Logic remains the same: extracting facts from context]
        context = "\n\n".join([
            f"Source [{i+1}] ({result['url']}):\n{result['content']}"
            for i, result in enumerate(search_results)
        ])
        
        research_prompt = f"""
        Extract every key fact, date, and technical specification from the search results below.
        
        ### Context:
        {context}
        
        ### User Query:
        {query}
        
        ### Instructions:
        1. List the findings as a detailed series of factual points.
        2. Keep the Source ID [number] attached to every single point.
        3. Factual only. No conversation.
        
        Factual Summary:"""
        
        research_chain = PromptTemplate.from_template(research_prompt) | self.research_llm | StrOutputParser()
        return research_chain.invoke({})

    def final_answer(self, raw_facts: str, query: str):
        # [Logic remains the same: synthesizing facts into a report]
        synthesis_prompt = f"Convert these research facts into a neat report: {raw_facts}\nQuery: {query}\nFinal Response:"
        synthesis_chain = PromptTemplate.from_template(synthesis_prompt) | self.synthesis_llm | StrOutputParser()
        return synthesis_chain.invoke({})