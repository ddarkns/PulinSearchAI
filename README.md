# PulinSearch AI 

**PulinSearch** is basicly a perplexity-like AI based chatbot. This mini-project uses a hybrid retrieval strategy by combining keyword-based matching (BM25) and semantic meaning of sentences (vector embeddings). Therefore providing a more context aware answer than a normal search query

Then finally to curate a answer for the users query a dual LLM architure is used , where  Qwen3 8B local model for extracting the relevant facts from the given context and
Llama 3.3 versatile model for formatting the final answer.



---

## Features:-

* **Hybrid Search Engine**: Combines **Semantic Search (70%)** for intent and **BM25 Keyword Matching (30%)** for technical terms and exact matches.
* **Intelligent Chunking**: Utilizes **Statistical Chunking** to break down web content into contextually meaningful pieces rather than arbitrary character counts.
* **Dual-LLM Pipeline**:
    * **Local Research**: Uses `Qwen3:8b` (via Ollama) to extract granular facts locally, ensuring data processing efficiency.
    * **Cloud Synthesis**: Uses `Llama-3.3-70b-versatile` (via Groq) for high-speed, high-quality report generation.
* **Automated Web Scraping**: Parallel scraping using `Tavily API` and `Trafilatura` for clean, noise-free text extraction.
* **Similarity Re-ranking**: Scores and sorts search results to ensure only the most relevant context is fed to the LLM.

---

## Tech Stack:-

### Backend
*  FastAPI (Python) for backend 
*  LangChain, LangChain-Groq and LangChain-Ollama 
*  Tavily API, Trafilatura, HTTPX for Search/Scraping
*  HuggingFace, Sentence Transformers for Vector Embeddings
*  Semantic Router for semantic chunking , BM25 (Rank-BM25) for keyword matching
*  Sklearn for sorting search results based on cosine similarity
* UV package manager

### Frontend
*  Next.js 14+ (App Router)
*  Tailwind CSS
*  Lucide React

---

## Project Preview:-

will add photos here later

---

## How To Install:-

### Prerequisites
* Install **UV** package manager (faster than pip)
* **Ollama** for running local LLM models
* **Node.js** and **npm** for the frontend

### 1. Clone the Repository
```bash
git clone (https://github.com/ddarkns/PulinSearchAI)
cd PulinSearchAI
```

### 2. Create a .env file in the root directory:
```bash
TAVILY_API_KEY=your_tavily_key 
GROQ_API_KEY=your_groq_key
```
### 3. backend setup
```bash
# Add/Install requirements using uv
uv pip install -r requirements.txt

# Start the FastAPI server
cd backend
uv run uvicorn main:app --reload
```
### 4. frontend setup
```bash
cd frontend
npm install
npm run dev
#The application will be available at http://localhost:3000.
```
