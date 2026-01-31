import React from 'react';

// This tells TypeScript what a 'source' looks like
interface Source {
  title: string;
  url: string;
}

export const SourceCard = ({ source }: { source: Source }) => {
  const domain = new URL(source.url).hostname;
  
  return (
    <a
      href={source.url}
      target="_blank"
      className="group flex flex-col p-3 bg-[#111] border border-white/5 rounded-xl hover:bg-[#161616] hover:border-white/10 transition-all duration-200"
    >
      <div className="flex items-center gap-2 mb-2">
        <img 
          src={`https://www.google.com/s2/favicons?sz=64&domain=${domain}`} 
          className="w-4 h-4 rounded-sm grayscale group-hover:grayscale-0 transition-all" 
          alt="" 
        />
        <span className="text-[10px] text-zinc-500 truncate font-mono uppercase tracking-tight">
          {domain}
        </span>
      </div>
      <p className="text-sm font-medium text-zinc-300 line-clamp-1 group-hover:text-blue-400">
        {source.title}
      </p>
    </a>
  );
};