import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { SourceCard } from './SourceCard';
import { Globe } from 'lucide-react';

interface Source {
  id: number;
  title: string;
  url: string;
}

interface AnswerSectionProps {
  result: {
    answer: string;
    sources: Source[];
  };
}

export const AnswerSection = ({ result }: AnswerSectionProps) => {
  return (
    <div className="w-full max-w-3xl mx-auto mt-12 space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-1000">
      {/* Sources Grid - Clean and Compact */}
      <div className="space-y-4">
        <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-500 flex items-center gap-2">
          <Globe size={12} /> Sources Found
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {result.sources.slice(0, 6).map((source, i) => (
            <SourceCard key={i} source={source} />
          ))}
        </div>
      </div>

      {/* Main Content - High-End Typography */}
      <div className="prose prose-invert prose-blue max-w-none 
        prose-p:text-zinc-300 prose-p:leading-relaxed prose-p:mb-6
        prose-headings:text-white prose-headings:font-bold prose-h2:text-2xl prose-h2:mt-10 prose-h2:mb-4
        prose-strong:text-white prose-strong:font-semibold
        prose-ul:list-disc prose-ul:pl-6 prose-li:mb-2">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {result.answer}
        </ReactMarkdown>
      </div>
    </div>
  );
};