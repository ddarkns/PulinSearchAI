import React from 'react';
import { Search, Sparkles, Globe } from "lucide-react";

interface SearchBarProps {
  query: string;
  setQuery: (query: string) => void;
  onSearch: () => void; // Changed: no longer takes mode as argument
  loading: boolean;
  currentMode: 'normal' | 'advanced';
  setMode: (mode: 'normal' | 'advanced') => void;
}

export const SearchBar = ({ query, setQuery, onSearch, loading, currentMode, setMode }: SearchBarProps) => {
  return (
    <div className="relative w-full max-w-3xl mx-auto space-y-4">
      <div className="relative group rounded-2xl bg-[#111] border border-white/5 focus-within:border-blue-500/50 transition-all duration-300 shadow-2xl">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              onSearch();
            }
          }}
          placeholder="Ask anything..."
          className="w-full bg-transparent p-6 pr-14 outline-none resize-none text-lg placeholder:text-zinc-600 min-h-[140px]"
        />
        <button
          onClick={onSearch}
          disabled={loading || !query.trim()}
          className="absolute bottom-4 right-4 p-3 bg-blue-600 rounded-xl hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-blue-500/20 text-white"
        >
          {loading ? (
            <div className="animate-spin h-5 w-5 border-2 border-white/30 border-t-white rounded-full" />
          ) : (
            <Search size={20} />
          )}
        </button>
      </div>

      <div className="flex items-center justify-center gap-6 text-sm">
        {/* Toggle Button: Normal */}
        <button 
          onClick={() => setMode('normal')} 
          className={`flex items-center gap-2 transition-colors duration-200 ${
            currentMode === 'normal' ? 'text-blue-500 font-semibold' : 'text-zinc-500 hover:text-zinc-200'
          }`}
        >
          <Globe size={14} className={currentMode === 'normal' ? 'text-blue-500' : ''} /> 
          Search
        </button>

        {/* Toggle Button: Advanced */}
        <button 
          onClick={() => setMode('advanced')} 
          className={`flex items-center gap-2 transition-colors duration-200 ${
            currentMode === 'advanced' ? 'text-blue-500 font-semibold' : 'text-zinc-500 hover:text-zinc-200'
          }`}
        >
          <Sparkles size={14} className={currentMode === 'advanced' ? 'text-blue-500' : ''} /> 
          Research (Hybrid)
        </button>
      </div>
    </div>
  );
};