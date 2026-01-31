import os
from typing import List
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import Settings

settings = Settings()

class LLMService:
    def __init__(self):
       
        self.research_llm = ChatOllama(
            model="qwen3:8b", 
            temperature=0.1,
            num_ctx=16384, 
            num_gpu=35 
        )

   
        self.synthesis_llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=settings.GROQ_API_KEY,
            temperature=0.2
        )

    async def generate_response(self, query: str, search_results: List[dict]):
        context = "\n\n".join([
            f"Source [{i+1}] ({result['url']}):\n{result['content']}"
            for i, result in enumerate(search_results)
        ])
        
        research_prompt = f"""
        Extract every key fact, date, and technical specification from the search results below.
        ### Context: {context}
        ### User Query: {query}
        ### Instructions:
        1. List findings as factual points.
        2. Keep Source link [URL] on every point.
        3. Factual only. No conversation.
        Factual Summary:"""
        
        chain = PromptTemplate.from_template(research_prompt) | self.research_llm | StrOutputParser()
        return await chain.ainvoke({}) # Async invoke

    async def final_answer(self, raw_facts: str, query: str):
        synthesis_prompt = f"""
        Convert these facts into a professional report with ## Headers and **bolding**.
        Preserve citations like ['sample.url'], ['sample2.url'] dont make these up use only the once which are given for the respective text.
        ### Facts: {raw_facts}
        ### Query: {query}
        Final Response:"""
        
        chain = PromptTemplate.from_template(synthesis_prompt) | self.synthesis_llm | StrOutputParser()
        return await chain.ainvoke({}) # Async invoke