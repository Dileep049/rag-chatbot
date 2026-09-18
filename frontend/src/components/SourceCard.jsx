import React, { useState } from 'react';
import { FileText, BookOpen, ExternalLink, ChevronDown, ChevronUp } from 'lucide-react';

export default function SourceCard({ source }) {
  const [expanded, setExpanded] = useState(false);

  if (!source) return null;

  const { document, page, category, section, excerpt, source_url } = source;

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-3.5 space-y-2 text-xs text-slate-300 shadow-sm transition hover:border-slate-700">
      
      {/* Header with Document Name */}
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center space-x-2 font-semibold text-slate-100 truncate">
          <FileText className="w-4 h-4 text-indigo-400 shrink-0" />
          <span className="truncate">{document || 'Official Document'}</span>
        </div>
        {category && (
          <span className="px-2 py-0.5 rounded-full text-[10px] font-medium uppercase tracking-wider bg-slate-800 text-indigo-300 border border-indigo-500/20 shrink-0">
            {category}
          </span>
        )}
      </div>

      {/* Metadata Row */}
      <div className="flex flex-wrap gap-x-4 gap-y-1 text-slate-400 text-[11px]">
        {page && (
          <div>
            <span className="font-medium text-slate-300">Page:</span> {page}
          </div>
        )}
        {section && (
          <div>
            <span className="font-medium text-slate-300">Section:</span> {section}
          </div>
        )}
      </div>

      {/* Optional Collapsible Excerpt */}
      {excerpt && (
        <div className="pt-1">
          <button
            onClick={() => setExpanded(!expanded)}
            className="flex items-center space-x-1 text-[11px] font-medium text-indigo-400 hover:text-indigo-300 transition"
          >
            <BookOpen className="w-3 h-3" />
            <span>{expanded ? 'Hide Excerpt' : 'View Excerpt'}</span>
            {expanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
          </button>

          {expanded && (
            <div className="mt-2 p-2.5 rounded-lg bg-slate-950/70 border border-slate-800 text-[11px] font-mono text-slate-300 whitespace-pre-wrap leading-relaxed">
              {excerpt}
            </div>
          )}
        </div>
      )}

      {/* Official Source Link (only shown if real source_url exists) */}
      {source_url && source_url.trim() && (
        <div className="pt-1">
          <a
            href={source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-1 px-2.5 py-1 rounded-lg bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 hover:bg-indigo-600/30 text-[11px] font-medium transition"
          >
            <span>Official Source →</span>
          </a>
        </div>
      )}

    </div>
  );
}
