"use client";

import { useState } from "react";
import { SearchBar } from "@/components/ui/SearchBar";
import { AnswerSection } from "@/components/ui/AnswerSection";
import { Sparkles } from "lucide-react";
import { askAI, SearchResponse } from "@/lib/api";

export default function Home() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [searchMode, setSearchMode] = useState<'normal' | 'advanced'>('advanced');

  const handleSearch = async () => {
    if (!query.trim() || loading) return;
    
    setLoading(true);
    setResult(null); 
    
    try {
      const data = await askAI(query, searchMode);
      setResult(data);
    } catch (err) {
      console.error("Search failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex-1 flex flex-col items-center px-6 py-12 md:py-24 max-w-5xl mx-auto w-full">
      {/* Header Section */}
      <div className={`transition-all duration-1000 w-full flex flex-col items-center ${result ? 'mb-12' : 'mb-20 mt-20'}`}>
        <div className="flex items-center gap-3 text-4xl font-bold tracking-tighter mb-4">
          <Sparkles className="text-blue-500 w-10 h-10" />
          <h1 className="bg-clip-text text-transparent bg-gradient-to-b from-white to-zinc-500">
            PulinSearch
          </h1>
        </div>
        {!result && (
          <p className="text-zinc-500 text-center max-w-md text-lg leading-relaxed">
            Deep research engine powered by Qwen3. <br/> 
            Faster, cleaner, and strictly factual.
          </p>
        )}
      </div>

      {/* Search Container */}
      <div className="w-full max-w-3xl">
        <SearchBar 
          query={query} 
          setQuery={setQuery} 
          onSearch={handleSearch} 
          loading={loading}
          currentMode={searchMode}
          setMode={setSearchMode}
        />
      </div>

      {/* Results Section */}
      <div className="w-full pb-20">
        {result && <AnswerSection result={result} />}

        {loading && (
          <div className="max-w-3xl w-full mx-auto mt-16 space-y-8 animate-pulse">
            <div className="h-4 bg-zinc-800/50 rounded-full w-3/4"></div>
            <div className="space-y-3">
              <div className="h-4 bg-zinc-800/50 rounded-full w-full"></div>
              <div className="h-4 bg-zinc-800/50 rounded-full w-5/6"></div>
            </div>
            <div className="grid grid-cols-3 gap-4 pt-6">
              <div className="h-20 bg-zinc-900/50 rounded-2xl border border-white/5"></div>
              <div className="h-20 bg-zinc-900/50 rounded-2xl border border-white/5"></div>
              <div className="h-20 bg-zinc-900/50 rounded-2xl border border-white/5"></div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}